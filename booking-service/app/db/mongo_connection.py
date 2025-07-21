from pymongo import MongoClient
import os
import logging

logger = logging.getLogger(__name__)

class MongoConnection:
    def __init__(self):
        self.client = None
        self.database = None
        self.connection_string = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        self.database_name = os.environ.get('MONGO_DATABASE', 'bookings_db')
    
    def connect(self):
        try:
            self.client = MongoClient(
                self.connection_string,
                connectTimeoutMS=5000,
                serverSelectionTimeoutMS=5000
            )
            self.database = self.client[self.database_name]
            # Verificación explícita de conexión
            self.client.admin.command('ping')
            logger.info("MongoDB connection established")
            return True
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            self.database = None
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def get_collection(self, collection_name: str):
        if self.database is None:  # Cambio clave aquí
            if not self.connect():
                raise ConnectionError("Could not connect to MongoDB")
        return self.database[collection_name]