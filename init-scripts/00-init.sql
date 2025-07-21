-- init-scripts/01-create-databases.sql
-- Script para crear las bases de datos necesarias

-- Crear base de datos para auth-service
CREATE DATABASE auth_db;

-- Crear base de datos para package-service
CREATE DATABASE packages_db;

-- Conectar a packages_db para crear tablas
\c packages_db;

-- Crear extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla de paquetes
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

-- Crear índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_packages_active ON packages(is_active);
CREATE INDEX IF NOT EXISTS idx_packages_location ON packages(location);
CREATE INDEX IF NOT EXISTS idx_packages_price ON packages(price);

-- Función para actualizar timestamp automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS '
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
' language plpgsql;

-- Trigger para actualizar updated_at automáticamente
CREATE TRIGGER update_packages_updated_at
    BEFORE UPDATE ON packages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insertar datos de ejemplo
INSERT INTO packages (name, description, price, duration_days, max_participants, location, includes, available_from, available_to) 
VALUES 
    (
        'Tour Centro Histórico de Quito',
        'Recorrido por las iglesias y plazas más emblemáticas del centro histórico de Quito, Patrimonio de la Humanidad.',
        45.99,
        1,
        15,
        'Centro Histórico, Quito',
        ARRAY['Guía turístico certificado', 'Transporte local', 'Entrada a iglesias', 'Mapa y material informativo'],
        '2025-01-01',
        '2025-12-31'
    ),
    (
        'Mitad del Mundo y Pululahua',
        'Visita al monumento ecuatorial y al cráter del volcán Pululahua con almuerzo típico incluido.',
        65.00,
        1,
        20,
        'Mitad del Mundo, Quito',
        ARRAY['Transporte ida y vuelta', 'Guía especializado', 'Entrada al museo', 'Almuerzo típico', 'Actividades interactivas'],
        '2025-01-01',
        '2025-12-31'
    ),
    (
        'TelefériQo y Cruz Loma',
        'Ascenso en teleférico hasta los 4,100 metros de altura con vistas panorámicas de Quito y los volcanes.',
        55.50,
        1,
        12,
        'TelefériQo, Quito',
        ARRAY['Boleto del teleférico', 'Guía de montaña', 'Equipo de seguridad', 'Refrigerio', 'Seguro de accidentes'],
        '2025-01-01',
        '2025-12-31'
    ),
    (
        'Quito Colonial Nocturno',
        'Tour nocturno por el centro histórico de Quito con iluminación especial y cena en restaurante tradicional.',
        75.00,
        1,
        10,
        'Centro Histórico, Quito',
        ARRAY['Guía nocturno especializado', 'Transporte privado', 'Cena típica', 'Bebidas tradicionales', 'Espectáculo folclórico'],
        '2025-01-01',
        '2025-12-31'
    ),
    (
        'Mercados y Gastronomía Quiteña',
        'Recorrido gastronómico por mercados tradicionales con degustación de platos típicos ecuatorianos.',
        40.00,
        1,
        8,
        'Mercados de Quito',
        ARRAY['Guía gastronómico', 'Degustaciones múltiples', 'Recetario digital', 'Transporte entre mercados'],
        '2025-01-01',
        '2025-12-31'
    );

-- Verificar datos insertados
SELECT COUNT(*) as total_packages FROM packages WHERE is_active = true;

-- Conectar a auth_db para crear tabla de usuarios (si tu auth-service la necesita)
\c auth_db;

-- Crear extensión UUID para auth_db también
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla de usuarios (ajustar según tu auth-service)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insertar usuario administrador de ejemplo
-- Nota: La contraseña debe ser hasheada por tu auth-service
INSERT INTO users (email, password_hash, is_admin) 
VALUES ('admin@email.com', '$2b$12$example_hash_here', true)
ON CONFLICT (email) DO NOTHING;