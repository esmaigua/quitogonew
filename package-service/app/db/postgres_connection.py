import psycopg2
import psycopg2.extras
import os
import logging

logger = logging.getLogger(__name__)

class PostgresConnection:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': os.environ.get('PG_HOST', 'localhost'),
            'database': os.environ.get('PG_DATABASE', 'packages_db'),
            'user': os.environ.get('PG_USER', 'postgres'),
            'password': os.environ.get('PG_PASSWORD', 'postgres'),
            'port': int(os.environ.get('PG_PORT', 5432))
        }
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.config)
            self.connection.autocommit = True
            logger.info("PostgreSQL connection established")
            self._create_tables()
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL connection closed")
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        if not self.connection:
            self.connect()
        
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            return cursor.rowcount
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()
    
    def _create_tables(self):
        """Crear tablas si no existen"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS packages (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL CHECK (price > 0),
            duration_days INTEGER NOT NULL CHECK (duration_days > 0),
            max_participants INTEGER NOT NULL CHECK (max_participants > 0),
            location VARCHAR(255) NOT NULL,
            includes TEXT[],
            available_from DATE,
            available_to DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );

        CREATE INDEX IF NOT EXISTS idx_packages_active ON packages(is_active);
        CREATE INDEX IF NOT EXISTS idx_packages_location ON packages(location);
        """
        self.execute_query(create_table_query)