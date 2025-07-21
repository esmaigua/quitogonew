import os
import requests
import consul
from functools import wraps
from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(self):
        self.consul_client = consul.Consul(
            host=os.environ.get('CONSUL_HOST', 'localhost'),
            port=int(os.environ.get('CONSUL_PORT', 8500))
        )
    
    def discover_auth_service(self):
        """Descubrir auth-service vía Consul"""
        try:
            services = self.consul_client.health.service('auth-service', passing=True)
            if services[1]:
                service = services[1][0]['Service']
                return f"http://{service['Address']}:{service['Port']}"
            else:
                logger.error("Auth service not found in Consul")
                return None
        except Exception as e:
            logger.error(f"Error discovering auth service: {e}")
            return None
    
    def verify_token(self, token: str):
        """Verificar token con auth-service"""
        auth_url = self.discover_auth_service()
        if not auth_url:
            return None
        
        try:
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.get(f"{auth_url}/me", headers=headers, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None

auth_middleware = AuthMiddleware()

def require_auth(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        # Extraer token del header "Bearer <token>"
        token = token.split(' ')[1] if token.startswith('Bearer ') else token
        user = auth_middleware.verify_token(token)
        
        if not user:
            return jsonify({'error': 'Invalid token'}), 401
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

def require_admin(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'current_user') or not request.current_user.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    
    return decorated_function