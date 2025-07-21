from abc import ABC, abstractmethod
from typing import List, Optional
from app.dto.package_dto import PackageDTO

class PackageRepository(ABC):
    """Interface abstracta para el repositorio de paquetes"""
    
    @abstractmethod
    def create(self, package: PackageDTO) -> PackageDTO:
        pass
    
    @abstractmethod
    def find_by_id(self, package_id: str) -> Optional[PackageDTO]:
        pass
    
    @abstractmethod
    def find_all(self) -> List[PackageDTO]:
        pass
    
    @abstractmethod
    def update(self, package: PackageDTO) -> PackageDTO:
        pass
    
    @abstractmethod
    def delete(self, package_id: str) -> bool:
        pass