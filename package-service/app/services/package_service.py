import datetime
from typing import List, Optional
from app.dto.package_dto import PackageDTO
from app.repositories.package_repository import PackageRepository
import logging

logger = logging.getLogger(__name__)

class PackageService:
    """Servicio de lógica de negocio para paquetes"""
    
    def __init__(self, package_repository: PackageRepository):
        self.package_repository = package_repository
    
    def create_package(self, package_data: dict) -> PackageDTO:
        """Crear un nuevo paquete turístico"""
        package = PackageDTO.from_dict(package_data)
        return self.package_repository.create(package)
    
    def get_all_packages(self) -> List[PackageDTO]:
        """Obtener todos los paquetes activos"""
        return self.package_repository.find_all()
    
    def get_available_packages(self) -> List[PackageDTO]:
        """Obtener solo paquetes disponibles (público)"""
        now = datetime.utcnow().isoformat()
        return self.package_repository.find_available(now)
    
    def get_package_by_id(self, package_id: str) -> Optional[PackageDTO]:
        """Obtener paquete por ID"""
        return self.package_repository.find_by_id(package_id)
    
    def update_package(self, package_id: str, package_data: dict) -> Optional[PackageDTO]:
        """Actualizar paquete existente"""
        existing_package = self.package_repository.find_by_id(package_id)
        if not existing_package:
            return None
        
        # Actualizar campos
        for key, value in package_data.items():
            if hasattr(existing_package, key):
                setattr(existing_package, key, value)
        
        return self.package_repository.update(existing_package)
    
    def delete_package(self, package_id: str) -> bool:
        """Eliminar paquete (soft delete)"""
        return self.package_repository.delete(package_id)