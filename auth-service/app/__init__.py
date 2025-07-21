from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración desde clase Config
    from config import Config
    app.config.from_object(Config)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Inicializar extensiones
    db.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from .routes import auth_bp
    app.register_blueprint(auth_bp)
    
    # Verificar conexión a la DB al iniciar
    with app.app_context():
        try:
            db.engine.connect()
            logger.info("Database connection verified")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise
    
    return app