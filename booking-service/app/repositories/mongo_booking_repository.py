from typing import List, Optional, Dict
from app.repositories.booking_repository import BookingRepository
from app.dto.booking_dto import BookingDTO
from app.db.mongo_connection import MongoConnection
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MongoBookingRepository(BookingRepository):
    """Implementación MongoDB del repositorio de reservas"""
    
    def __init__(self, db_connection: MongoConnection):
        self.db = db_connection
        self.collection = self.db.get_collection('bookings')
    
    def create(self, booking: BookingDTO) -> BookingDTO:
        booking_dict = booking.to_dict()
        self.collection.insert_one(booking_dict)
        return booking
    
    def find_by_id(self, booking_id: str) -> Optional[BookingDTO]:
        result = self.collection.find_one({"id": booking_id})
        if result:
            result.pop('_id', None)  # Remove MongoDB's _id
            return BookingDTO.from_dict(result)
        return None
    
    def find_by_user_id(self, user_id: str) -> List[BookingDTO]:
        results = self.collection.find({"user_id": user_id})
        bookings = []
        for result in results:
            result.pop('_id', None)
            bookings.append(BookingDTO.from_dict(result))
        return bookings
    
    def find_all(self) -> List[BookingDTO]:
        results = self.collection.find({})
        bookings = []
        for result in results:
            result.pop('_id', None)
            bookings.append(BookingDTO.from_dict(result))
        return bookings
    
    def update(self, booking: BookingDTO) -> BookingDTO:
        booking.updated_at = datetime.utcnow().isoformat()
        booking_dict = booking.to_dict()
        self.collection.update_one(
            {"id": booking.id},
            {"$set": booking_dict}
        )
        return booking
    
    def delete(self, booking_id: str) -> bool:
        result = self.collection.update_one(
            {"id": booking_id},
            {"$set": {"status": "cancelled", "updated_at": datetime.utcnow().isoformat()}}
        )
        return result.modified_count > 0
    
    def get_bookings_report(self, start_date: str, end_date: str) -> List[Dict]:
        pipeline = [
            {
                "$match": {
                    "booking_date": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$package_id",
                    "total_bookings": {"$sum": 1},
                    "total_participants": {"$sum": "$participants"},
                    "total_revenue": {"$sum": "$total_amount"},
                    "avg_participants": {"$avg": "$participants"}
                }
            },
            {
                "$sort": {"total_revenue": -1}
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        for result in results:
            result['package_id'] = result.pop('_id')
        
        return results