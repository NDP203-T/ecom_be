from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.product_controller import ProductController
from app.middleware.auth import admin_required
from app.middleware.validation import validate_json
from app.middleware.encryption import encrypt_response

bp = Blueprint('product', __name__, url_prefix='/api/products')

@bp.route('', methods=['GET'])
@encrypt_response()
def get_all_products():
    """Lấy danh sách sản phẩm (public)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category', None)
    is_active = request.args.get('is_active', None)
    
    result, status_code = ProductController.get_all_products(page, per_page, category, is_active)
    return jsonify(result), status_code

@bp.route('/<product_id>', methods=['GET'])
@encrypt_response()
def get_product(product_id):
    """Lấy chi tiết sản phẩm (public)"""
    result, status_code = ProductController.get_product_by_id(product_id)
    return jsonify(result), status_code

@bp.route('/add', methods=['POST'])
@jwt_required()
@admin_required
@validate_json('name', 'price')
@encrypt_response()
def create_product():
    """Tạo sản phẩm mới (Admin only)"""
    data = request.get_json()
    result, status_code = ProductController.create_product(data)
    return jsonify(result), status_code

@bp.route('/<product_id>', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def update_product(product_id):
    """Cập nhật sản phẩm (Admin only)"""
    data = request.get_json()
    result, status_code = ProductController.update_product(product_id, data)
    return jsonify(result), status_code

@bp.route('/<product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@encrypt_response()
def delete_product(product_id):
    """Xóa sản phẩm (Admin only)"""
    result, status_code = ProductController.delete_product(product_id)
    return jsonify(result), status_code

@bp.route('/<product_id>/toggle-status', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def toggle_product_status(product_id):
    """Ẩn/hiện sản phẩm (Admin only)"""
    result, status_code = ProductController.toggle_product_status(product_id)
    return jsonify(result), status_code

@bp.route('/<product_id>/stock', methods=['PUT'])
@jwt_required()
@admin_required
@validate_json('stock')
@encrypt_response()
def update_stock(product_id):
    """Cập nhật tồn kho (Admin only)"""
    data = request.get_json()
    result, status_code = ProductController.update_stock(product_id, data['stock'])
    return jsonify(result), status_code

# === Image Management ===
@bp.route('/<product_id>/images', methods=['POST'])
@jwt_required()
@admin_required
@encrypt_response()
def upload_product_image(product_id):
    """Upload ảnh sản phẩm (Admin only)"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    image = request.files['image']
    is_primary = request.form.get('is_primary', 'false').lower() == 'true'
    
    result, status_code = ProductController.upload_image(product_id, image, is_primary)
    return jsonify(result), status_code

@bp.route('/<product_id>/images/<image_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@encrypt_response()
def delete_product_image(product_id, image_id):
    """Xóa ảnh sản phẩm (Admin only)"""
    result, status_code = ProductController.delete_image(product_id, image_id)
    return jsonify(result), status_code

# === Variant Management ===
@bp.route('/<product_id>/variants', methods=['POST'])
@jwt_required()
@admin_required
@validate_json('sku', 'name')
@encrypt_response()
def create_variant(product_id):
    """Tạo biến thể sản phẩm (Admin only)"""
    data = request.get_json()
    result, status_code = ProductController.create_variant(product_id, data)
    return jsonify(result), status_code

@bp.route('/<product_id>/variants/<variant_id>', methods=['PUT'])
@jwt_required()
@admin_required
@encrypt_response()
def update_variant(product_id, variant_id):
    """Cập nhật biến thể (Admin only)"""
    data = request.get_json()
    result, status_code = ProductController.update_variant(product_id, variant_id, data)
    return jsonify(result), status_code

@bp.route('/<product_id>/variants/<variant_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@encrypt_response()
def delete_variant(product_id, variant_id):
    """Xóa biến thể (Admin only)"""
    result, status_code = ProductController.delete_variant(product_id, variant_id)
    return jsonify(result), status_code
