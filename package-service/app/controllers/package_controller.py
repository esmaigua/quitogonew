from flask import Blueprint, request, jsonify
from app.services.package_service import PackageService
from app.factories.repository_factory import RepositoryFactory
from app.auth.auth_middleware import require_auth, require_admin
import logging

logger = logging.getLogger(__name__)

# Crear blueprint
package_bp = Blueprint('packages', __name__)

# Inicializar servicio
package_service = PackageService(RepositoryFactory.create_package_repository())

@package_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'package-service'})

@package_bp.route('/packages', methods=['POST'])
@require_auth
@require_admin
def create_package():
    """Crear nuevo paquete turístico"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validar campos requeridos
        required_fields = ['name', 'description', 'price', 'duration_days', 'max_participants', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validar tipos de datos
        if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
            return jsonify({'error': 'Price must be a positive number'}), 400
        
        if not isinstance(data['duration_days'], int) or data['duration_days'] <= 0:
            return jsonify({'error': 'Duration days must be a positive integer'}), 400
        
        if not isinstance(data['max_participants'], int) or data['max_participants'] <= 0:
            return jsonify({'error': 'Max participants must be a positive integer'}), 400
        
        package = package_service.create_package(data)
        return jsonify({
            'message': 'Package created successfully',
            'package': package.to_dict()
        }), 201
    
    except Exception as e:
        logger.error(f"Error creating package: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@package_bp.route('/packages', methods=['GET'])
@require_auth
def get_packages():
    """Listar todos los paquetes (disponible para todos los usuarios autenticados)"""
    try:
        packages = package_service.get_all_packages()
        return jsonify({
            'packages': [package.to_dict() for package in packages],
            'total': len(packages)
        })
    except Exception as e:
        logger.error(f"Error getting packages: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@package_bp.route('/packages/public', methods=['GET'])
def get_public_packages():
    """Listar paquetes disponibles (sin autenticación)"""
    try:
        packages = package_service.get_available_packages()
        return jsonify({
            'packages': [package.to_dict() for package in packages],
            'total': len(packages)
        })
    except Exception as e:
        logger.error(f"Error getting public packages: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@package_bp.route('/packages/<package_id>', methods=['PUT'])
@require_auth
@require_admin
def update_package(package_id):
    """Actualizar paquete turístico"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validar tipos de datos si están presentes
        if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] <= 0):
            return jsonify({'error': 'Price must be a positive number'}), 400
        
        if 'duration_days' in data and (not isinstance(data['duration_days'], int) or data['duration_days'] <= 0):
            return jsonify({'error': 'Duration days must be a positive integer'}), 400
        
        if 'max_participants' in data and (not isinstance(data['max_participants'], int) or data['max_participants'] <= 0):
            return jsonify({'error': 'Max participants must be a positive integer'}), 400
        
        package = package_service.update_package(package_id, data)
        if not package:
            return jsonify({'error': 'Package not found'}), 404
        
        return jsonify({
            'message': 'Package updated successfully',
            'package': package.to_dict()
        })
    except Exception as e:
        logger.error(f"Error updating package: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@package_bp.route('/packages/<package_id>', methods=['DELETE'])
@require_auth
@require_admin
def delete_package(package_id):
    """Eliminar paquete turístico"""
    try:
        if package_service.delete_package(package_id):
            return jsonify({'message': 'Package deleted successfully'})
        else:
            return jsonify({'error': 'Package not found'}), 404
    except Exception as e:
        logger.error(f"Error deleting package: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
@package_bp.route('/packages/<package_id>', methods=['GET'])
def get_package_by_id(package_id):
    """Obtener un paquete específico por su ID"""
    try:
        package = package_service.get_package_by_id(package_id)
        if not package:
            return jsonify({'error': 'Package not found'}), 404
        return jsonify(package.to_dict()), 200
    except Exception as e:
        logger.error(f"Error getting package by ID: {e}")
        return jsonify({'error': 'Internal server error'}), 500
