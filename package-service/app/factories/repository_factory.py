from app.repositories.package_repository import PackageRepository
from app.repositories.postgres_package_repository import PostgresPackageRepository
from app.db.postgres_connection import PostgresConnection

class RepositoryFactory:
    """Factory para crear repositorios"""
    
    @staticmethod
    def create_package_repository() -> PackageRepository:
        db_connection = PostgresConnection()
        db_connection.connect()
        return PostgresPackageRepository(db_connection)
    
    @staticmethod
    def create_public_package_repository() -> PackageRepository:
        """Repositorio con acceso solo de lectura para endpoints públicos"""
        db_connection = PostgresConnection()
        db_connection.connect()
        return PostgresPackageRepository(db_connection)