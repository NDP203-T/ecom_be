from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.order_controller import OrderController
from app.middleware.auth import admin_required
from app.middleware.validation import validate_json
from app.middleware.encryption import encrypt_response

bp = Blueprint('order', __name__, url_prefix='/api/orders')

@bp.route('', methods=['POST'])
@jwt_required()
@validate_json('items', 'customer_name', 'customer_phone', 'shipping_address')
@encrypt_response()
def create_order():
    """Tạo đơn hàng mới (User)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    result, status_code = OrderController.create_order(user_id, data)
    return jsonify(result), status_code

@bp.route('/my-orders', methods=['GET'])
@jwt_required()
@encrypt_response()
def get_my_orders():
    """Lấy danh sách đơn hàng của user"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    result, status_code = OrderController.get_user_orders(user_id, page, per_page)
    return jsonify(result), status_code

@bp.route('/<order_id>', methods=['GET'])
@jwt_required()
@encrypt_response()
def get_order(order_id):
    """Lấy chi tiết đơn hàng (User)"""
    user_id = get_jwt_identity()
    result, status_code = OrderController.get_order_by_id(order_id, user_id)
    return jsonify(result), status_code

@bp.route('/number/<order_number>', methods=['GET'])
@jwt_required()
@encrypt_response()
def get_order_by_number(order_number):
    """Lấy đơn hàng theo order_number (User)"""
    user_id = get_jwt_identity()
    result, status_code = OrderController.get_order_by_number(order_number, user_id)
    return jsonify(result), status_code

@bp.route('/<order_id>/cancel', methods=['PUT'])
@jwt_required()
@encrypt_response()
def cancel_order(order_id):
    """Hủy đơn hàng (User)"""
    user_id = get_jwt_identity()
    result, status_code = OrderController.cancel_order(order_id, user_id)
    return jsonify(result), status_code

# === Admin endpoints ===

@bp.route('/admin/all', methods=['GET'])
@jwt_required()
@admin_required
@encrypt_response()
def get_all_orders():
    """Lấy tất cả đơn hàng (Admin)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)
    
    result, status_code = OrderController.get_all_orders(page, per_page, status)
    return jsonify(result), status_code

@bp.route('/admin/<order_id>', methods=['GET'])
@jwt_required()
@admin_required
@encrypt_response()
def admin_get_order(order_id):
    """Lấy chi tiết đơn hàng (Admin)"""
    result, status_code = OrderController.get_order_by_id(order_id)
    return jsonify(result), status_code

@bp.route('/admin/<order_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
@validate_json('status')
@encrypt_response()
def update_order_status(order_id):
    """Cập nhật trạng thái đơn hàng (Admin)"""
    data = request.get_json()
    result, status_code = OrderController.update_order_status(order_id, data['status'])
    return jsonify(result), status_code

@bp.route('/admin/<order_id>/note', methods=['PUT'])
@jwt_required()
@admin_required
@validate_json('note')
@encrypt_response()
def update_admin_note(order_id):
    """Cập nhật ghi chú admin (Admin)"""
    data = request.get_json()
    result, status_code = OrderController.update_admin_note(order_id, data['note'])
    return jsonify(result), status_code

@bp.route('/admin/<order_id>/cancel', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def admin_cancel_order(order_id):
    """Hủy đơn hàng (Admin)"""
    result, status_code = OrderController.cancel_order(order_id)
    return jsonify(result), status_code
