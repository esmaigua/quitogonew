import os
import logging
from app import create_app
from app.controllers.package_controller import package_bp
from consul_register import ConsulServiceRegistry

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Crear aplicación Flask
    app = create_app()
    
    # Registrar blueprints
    app.register_blueprint(package_bp)
    
    # Registrar servicio en Consul
    registry = ConsulServiceRegistry()
    registry.register_service()
    
    # Configuración del servidor
    host = os.environ.get('SERVICE_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVICE_PORT', 5002))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Package Service starting on {host}:{port}")
    
    # Iniciar aplicación
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()