import requests
import consul
import os
import logging

logger = logging.getLogger(__name__)

class PackageServiceClient:
    """Cliente para comunicarse con package-service"""
    
    def __init__(self):
        self.consul_client = consul.Consul(
            host=os.environ.get('CONSUL_HOST', 'localhost'),
            port=int(os.environ.get('CONSUL_PORT', 8500))
        )
    
    def discover_package_service(self):
        """Descubrir package-service vía Consul"""
        try:
            services = self.consul_client.health.service('package-service', passing=True)
            if services[1]:
                service = services[1][0]['Service']
                return f"http://{service['Address']}:{service['Port']}"
            else:
                logger.error("Package service not found in Consul")
                return None
        except Exception as e:
            logger.error(f"Error discovering package service: {e}")
            return None
    
    def get_package_by_id(self, package_id: str):
        """Obtener información de un paquete por ID"""
        package_url = self.discover_package_service()
        if not package_url:
            return None
        
        try:
            response = requests.get(f"{package_url}/packages/{package_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting package info: {e}")
            return None