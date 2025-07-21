from typing import List, Optional
from app.repositories.package_repository import PackageRepository
from app.dto.package_dto import PackageDTO
from app.db.postgres_connection import PostgresConnection
import logging

logger = logging.getLogger(__name__)

class PostgresPackageRepository(PackageRepository):
    """Implementación PostgreSQL del repositorio de paquetes"""
    
    def __init__(self, db_connection: PostgresConnection):
        self.db = db_connection
    
    def create(self, package: PackageDTO) -> PackageDTO:
        query = """
        INSERT INTO packages (name, description, price, duration_days, max_participants, 
                            location, includes, available_from, available_to)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id, created_at, updated_at
        """
        params = (
            package.name, package.description, package.price, package.duration_days,
            package.max_participants, package.location, package.includes,
            package.available_from, package.available_to
        )
        
        result = self.db.execute_query(query, params, fetch=True)
        if result:
            package.id = str(result[0]['id'])
            package.created_at = result[0]['created_at'].isoformat()
            package.updated_at = result[0]['updated_at'].isoformat()
        
        return package
    
    def find_by_id(self, package_id: str) -> Optional[PackageDTO]:
        query = """
        SELECT id, name, description, price, duration_days, max_participants,
               location, includes, available_from, available_to, 
               created_at, updated_at, is_active
        FROM packages WHERE id = %s AND is_active = TRUE
        """
        result = self.db.execute_query(query, (package_id,), fetch=True)
        
        if result:
            row = result[0]
            return PackageDTO(
                id=str(row['id']), name=row['name'], description=row['description'],
                price=float(row['price']), duration_days=row['duration_days'],
                max_participants=row['max_participants'], location=row['location'],
                includes=row['includes'] or [], 
                available_from=row['available_from'].isoformat() if row['available_from'] else "",
                available_to=row['available_to'].isoformat() if row['available_to'] else "",
                created_at=row['created_at'].isoformat(),
                updated_at=row['updated_at'].isoformat(),
                is_active=row['is_active']
            )
        return None
    
    def find_all(self) -> List[PackageDTO]:
        query = """
        SELECT id, name, description, price, duration_days, max_participants,
               location, includes, available_from, available_to, 
               created_at, updated_at, is_active
        FROM packages WHERE is_active = TRUE
        ORDER BY created_at DESC
        """
        result = self.db.execute_query(query, fetch=True)
        
        packages = []
        for row in result:
            packages.append(PackageDTO(
                id=str(row['id']), name=row['name'], description=row['description'],
                price=float(row['price']), duration_days=row['duration_days'],
                max_participants=row['max_participants'], location=row['location'],
                includes=row['includes'] or [],
                available_from=row['available_from'].isoformat() if row['available_from'] else "",
                available_to=row['available_to'].isoformat() if row['available_to'] else "",
                created_at=row['created_at'].isoformat(),
                updated_at=row['updated_at'].isoformat(),
                is_active=row['is_active']
            ))
        return packages
    
    def update(self, package: PackageDTO) -> PackageDTO:
        query = """
        UPDATE packages SET name = %s, description = %s, price = %s, 
                          duration_days = %s, max_participants = %s, location = %s,
                          includes = %s, available_from = %s, available_to = %s,
                          updated_at = CURRENT_TIMESTAMP
        WHERE id = %s AND is_active = TRUE
        RETURNING updated_at
        """
        params = (
            package.name, package.description, package.price, package.duration_days,
            package.max_participants, package.location, package.includes,
            package.available_from, package.available_to, package.id
        )
        
        result = self.db.execute_query(query, params, fetch=True)
        if result:
            package.updated_at = result[0]['updated_at'].isoformat()
        
        return package
    
    def delete(self, package_id: str) -> bool:
        query = "UPDATE packages SET is_active = FALSE WHERE id = %s"
        result = self.db.execute_query(query, (package_id,))
        return result > 0
    
    def find_available(self) -> List[PackageDTO]:
        """Obtener solo paquetes disponibles"""
        query = """
            SELECT * FROM packages 
            WHERE is_active = TRUE 
            AND available_from <= CURRENT_DATE 
            AND available_to >= CURRENT_DATE
        """
        results = self.db.execute_query(query, fetch=True)
        return [PackageDTO.from_dict(row) for row in results]
