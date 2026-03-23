from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.dashboard_controller import DashboardController
from app.middleware.auth import admin_required
from app.middleware.encryption import encrypt_response

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/overview', methods=['GET'])
@jwt_required()
@admin_required()
@encrypt_response()
def get_overview():
    """Lấy tổng quan dashboard - Chỉ admin"""
    result, status_code = DashboardController.get_overview()
    return jsonify(result), status_code
