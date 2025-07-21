from flask import Blueprint, request, jsonify
from app.services.booking_service import BookingService
from app.factories.repository_factory import RepositoryFactory
from app.auth.auth_middleware import require_auth, require_admin, require_user
from datetime import datetime
import logging
import requests

logger = logging.getLogger(__name__)

# Crear blueprint
booking_bp = Blueprint('bookings', __name__)

# Inicializar servicio
booking_service = BookingService(RepositoryFactory.create_booking_repository())

# URL del package-service
PACKAGE_SERVICE_URL = "http://package-service:5002"

def package_exists(package_id: str) -> bool:
    try:
        url = f"{PACKAGE_SERVICE_URL}/packages/{package_id}"
        logger.info(f"[package_exists] Consultando URL: {url}")

        response = requests.get(url, timeout=5)
        logger.info(f"[package_exists] Código respuesta: {response.status_code}")
        logger.info(f"[package_exists] Contenido respuesta: {response.text}")

        return response.status_code == 200
    except requests.RequestException as e:
        logger.warning(f"Error al consultar package-service: {e}")
        return False


@booking_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'booking-service'})

@booking_bp.route('/bookings', methods=['POST'])
@require_auth
@require_user
def create_booking():
    """Crear nueva reserva (usuarios)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['package_id', 'travel_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        if 'participants' in data and (not isinstance(data['participants'], int) or data['participants'] <= 0):
            return jsonify({'error': 'Participants must be a positive integer'}), 400

        try:
            datetime.fromisoformat(data['travel_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid travel_date format. Use ISO format.'}), 400

        # Validar existencia del paquete vía HTTP al package-service
        if not package_exists(data['package_id']):
            return jsonify({'error': 'Package not found'}), 404

        # Crear la reserva si todo es válido
        booking = booking_service.create_booking(data, request.current_user)
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201

    except Exception as e:
        logger.error(f"Error creating booking: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/bookings', methods=['GET'])
@require_auth
@require_user
def get_user_bookings():
    """Listar reservas del usuario actual"""
    try:
        bookings = booking_service.get_user_bookings(request.current_user['id'])
        return jsonify({
            'bookings': [booking.to_dict() for booking in bookings],
            'total': len(bookings)
        })
    except Exception as e:
        logger.error(f"Error getting user bookings: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/bookings/<booking_id>', methods=['DELETE'])
@require_auth
@require_user
def cancel_booking(booking_id):
    """Cancelar reserva"""
    try:
        if booking_service.cancel_booking(booking_id, request.current_user['id']):
            return jsonify({'message': 'Booking cancelled successfully'})
        else:
            return jsonify({'error': 'Booking not found or not authorized'}), 404
    except Exception as e:
        logger.error(f"Error cancelling booking: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@booking_bp.route('/bookings/report', methods=['GET'])
@require_auth
@require_admin
def get_bookings_report():
    """Obtener reporte de reservas (admin)"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({'error': 'start_date and end_date are required'}), 400

        try:
            datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use ISO format.'}), 400

        report = booking_service.get_bookings_report(start_date, end_date)
        return jsonify({
            'report': report,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'generated_at': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return jsonify({'error': 'Internal server error'}), 500
