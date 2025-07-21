from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
import uuid

@dataclass
class BookingDTO:
    """Data Transfer Object para reservas"""
    id: Optional[str] = None
    package_id: str = ""
    user_id: str = ""
    user_email: str = ""
    booking_date: str = ""
    travel_date: str = ""
    participants: int = 1
    total_amount: float = 0.0
    status: str = "pending"  # pending, confirmed, cancelled
    notes: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow().isoformat()
        if self.booking_date == "":
            self.booking_date = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)