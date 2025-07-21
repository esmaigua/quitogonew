from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.dto.booking_dto import BookingDTO

class BookingRepository(ABC):
    """Interface abstracta para el repositorio de reservas"""
    
    @abstractmethod
    def create(self, booking: BookingDTO) -> BookingDTO:
        pass
    
    @abstractmethod
    def find_by_id(self, booking_id: str) -> Optional[BookingDTO]:
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: str) -> List[BookingDTO]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[BookingDTO]:
        pass
    
    @abstractmethod
    def update(self, booking: BookingDTO) -> BookingDTO:
        pass
    
    @abstractmethod
    def delete(self, booking_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_bookings_report(self, start_date: str, end_date: str) -> List[Dict]:
        pass