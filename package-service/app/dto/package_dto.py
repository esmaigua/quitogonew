from dataclasses import dataclass, asdict, field
from typing import Optional, List
from datetime import datetime

@dataclass
class PackageDTO:
    """Data Transfer Object para paquetes turísticos"""
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    price: float = 0.0
    duration_days: int = 0
    max_participants: int = 0
    location: str = ""
    includes: List[str] = field(default_factory=list)
    available_from: str = ""
    available_to: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    is_active: bool = True
    cost_price: Optional[float] = None  # Campo interno no público
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    def to_public_dict(self):
        """Versión segura para mostrar al público"""
        data = self.to_dict()
        data.pop('cost_price', None)  # Eliminamos información interna
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)