from app.repositories.booking_repository import BookingRepository
from app.repositories.mongo_booking_repository import MongoBookingRepository
from app.db.mongo_connection import MongoConnection
import logging

logger = logging.getLogger(__name__)

class RepositoryFactory:
    """Factory para crear repositorios"""
    
    @staticmethod
    def create_booking_repository() -> BookingRepository:
        try:
            db_connection = MongoConnection()
            # Verificación explícita de conexión
            if not db_connection.connect():
                raise ConnectionError("Failed to connect to MongoDB")
            
            # Verificación adicional de que la colección existe
            collection = db_connection.get_collection('bookings')
            collection.find_one()  # Prueba simple de lectura
            
            return MongoBookingRepository(db_connection)
        except Exception as e:
            logger.error(f"Error creating booking repository: {e}")
            raise