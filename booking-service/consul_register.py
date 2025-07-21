import consul
import os
import time
import logging
import atexit

logger = logging.getLogger(__name__)

class ConsulServiceRegistry:
    def __init__(self):
        self.consul_client = consul.Consul(
            host=os.environ.get('CONSUL_HOST', 'localhost'),
            port=int(os.environ.get('CONSUL_PORT', 8500))
        )
        self.service_id = None
        self.is_registered = False
    
    def register_service(self):
        """Registrar servicio en Consul"""
        service_name = os.environ.get('SERVICE_NAME', 'booking-service')
        service_id = os.environ.get('SERVICE_ID', 'booking-service-1')
        service_host = os.environ.get('SERVICE_HOST', 'localhost')
        service_port = int(os.environ.get('SERVICE_PORT', 5003))
        
        try:
            service_config = {
                'name': service_name,
                'service_id': service_id,
                'address': service_host,
                'port': service_port,
                'check': {
                    'http': f'http://{service_host}:{service_port}/health',
                    'interval': '10s',
                    'timeout': '5s',
                    'deregister_critical_service_after': '30s'
                },
                'tags': ['bookings', 'microservice', 'api']
            }
            
            self.consul_client.agent.service.register(**service_config)
            self.service_id = service_id
            self.is_registered = True
            logger.info(f"Service {service_name} registered with ID {service_id}")
            
            # Registrar handler para cleanup
            atexit.register(self.deregister_service)
            
        except Exception as e:
            logger.error(f"Error registering service: {e}")
    
    def deregister_service(self):
        """Desregistrar servicio de Consul"""
        if self.is_registered and self.service_id:
            try:
                self.consul_client.agent.service.deregister(self.service_id)
                logger.info(f"Service {self.service_id} deregistered")
                self.is_registered = False
            except Exception as e:
                logger.error(f"Error deregistering service: {e}")