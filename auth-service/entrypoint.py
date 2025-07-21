import os  
import time
import logging
from app import create_app, db
from app.models import User
from consul_register import ConsulServiceRegistry

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_database():
    """Espera a que la base de datos esté disponible usando SQLAlchemy"""
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError
    
    MAX_RETRIES = 30
    db_url = os.getenv("DATABASE_URL")
    
    for i in range(MAX_RETRIES):
        try:
            engine = create_engine(db_url)
            conn = engine.connect()
            conn.close()
            logger.info("Database connection successful")
            return True
        except OperationalError as e:
            logger.info(f"Waiting for database... ({i+1}/{MAX_RETRIES})")
            time.sleep(1)
    
    logger.error("Could not connect to database")
    return False

def main():
    # Esperar base de datos
    if not wait_for_database():
        exit(1)
    
    # Crear aplicación
    app = create_app()
    
    # Crear tablas
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created")
            
            # Crear usuario admin si no existe
            if not User.query.filter_by(email="admin@example.com").first():
                from werkzeug.security import generate_password_hash
                admin = User(
                    email="admin@example.com",
                    password=generate_password_hash("admin123"),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin user created")
                
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            exit(1)
    
    # Registrar en Consul
    registry = ConsulServiceRegistry()
    registry.register_service()
    
    # Obtener configuración del servidor
    host = os.environ.get('SERVICE_HOST', '0.0.0.0')
    port = int(os.environ.get('SERVICE_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Auth Service starting on {host}:{port}")
    
    # Iniciar servidor
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()