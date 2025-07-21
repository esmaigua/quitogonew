from typing import List, Optional, Dict
from app.dto.booking_dto import BookingDTO
from app.repositories.booking_repository import BookingRepository
from app.services.package_service_client import PackageServiceClient
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BookingService:
    """Servicio de lógica de negocio para reservas"""
    
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository
        self.package_client = PackageServiceClient()
    
    def create_booking(self, booking_data: dict, user: dict) -> Optional[BookingDTO]:
        """Crear una nueva reserva"""
        # Verificar que el paquete existe
        package = self.package_client.get_package_by_id(booking_data['package_id'])
        if not package:
            return None
        
        # Calcular monto total
        participants = booking_data.get('participants', 1)
        total_amount = package['price'] * participants
        
        # Crear booking
        booking = BookingDTO(
            package_id=booking_data['package_id'],
            user_id=user['id'],
            user_email=user['email'],
            travel_date=booking_data.get('travel_date', ''),
            participants=participants,
            total_amount=total_amount,
            notes=booking_data.get('notes', ''),
            status='pending'
        )
        
        return self.booking_repository.create(booking)
    
    def get_user_bookings(self, user_id: str) -> List[BookingDTO]:
        """Obtener reservas de un usuario"""
        return self.booking_repository.find_by_user_id(user_id)
    
    def cancel_booking(self, booking_id: str, user_id: str) -> bool:
        """Cancelar una reserva"""
        booking = self.booking_repository.find_by_id(booking_id)
        if not booking or booking.user_id != user_id:
            return False
        
        return self.booking_repository.delete(booking_id)
    
    def get_bookings_report(self, start_date: str, end_date: str) -> List[Dict]:
        """Obtener reporte de reservas con información de paquetes"""
        report = self.booking_repository.get_bookings_report(start_date, end_date)
        
        # Enriquecer reporte con información de paquetes
        for item in report:
            package = self.package_client.get_package_by_id(item['package_id'])
            if package:
                item['package_name'] = package['name']
                item['package_location'] = package['location']
            else:
                item['package_name'] = 'Unknown'
                item['package_location'] = 'Unknown'
        
        return report