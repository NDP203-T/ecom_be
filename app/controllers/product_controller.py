from app.services.product_service import ProductService
from app.services.cloudinary_service import CloudinaryService
import logging

logger = logging.getLogger(__name__)

class ProductController:
    
    @staticmethod
    def get_all_products(page=1, per_page=20, category=None, is_active=None):
        """Lấy danh sách sản phẩm với filter"""
        products, total = ProductService.get_all_products(page, per_page, category, is_active)
        
        return {
            'products': [product.to_dict(include_images=True) for product in products],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }, 200
    
    @staticmethod
    def get_product_by_id(product_id):
        """Lấy chi tiết sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        return {
            'product': product.to_dict(include_images=True, include_variants=True)
        }, 200
    
    @staticmethod
    def create_product(data):
        """Tạo sản phẩm mới"""
        # Validate price
        try:
            price = float(data['price'])
            if price < 0:
                return {'error': 'Price must be positive'}, 400
        except ValueError:
            return {'error': 'Invalid price format'}, 400
        
        # Validate stock
        stock = data.get('stock', 0)
        if stock < 0:
            return {'error': 'Stock must be non-negative'}, 400
        
        # Check SKU uniqueness
        if data.get('sku') and ProductService.get_product_by_sku(data['sku']):
            return {'error': 'SKU already exists'}, 400
        
        product = ProductService.create_product(data)
        
        logger.info(f"Product created: {product.id} - {product.name}")
        
        return {
            'message': 'Product created successfully',
            'product': product.to_dict()
        }, 201
    
    @staticmethod
    def update_product(product_id, data):
        """Cập nhật sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Validate price if provided
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    return {'error': 'Price must be positive'}, 400
            except ValueError:
                return {'error': 'Invalid price format'}, 400
        
        # Validate stock if provided
        if 'stock' in data and data['stock'] < 0:
            return {'error': 'Stock must be non-negative'}, 400
        
        # Check SKU uniqueness if changed
        if 'sku' in data and data['sku'] != product.sku:
            existing = ProductService.get_product_by_sku(data['sku'])
            if existing:
                return {'error': 'SKU already exists'}, 400
        
        updated_product = ProductService.update_product(product_id, data)
        
        logger.info(f"Product updated: {product_id}")
        
        return {
            'message': 'Product updated successfully',
            'product': updated_product.to_dict()
        }, 200
    
    @staticmethod
    def delete_product(product_id):
        """Xóa sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Xóa tất cả ảnh trên Cloudinary
        if product.image_url:
            CloudinaryService.delete_image_from_url(product.image_url)
        
        for image in product.images:
            CloudinaryService.delete_image_from_url(image.image_url)
        
        ProductService.delete_product(product_id)
        
        logger.info(f"Product deleted: {product_id}")
        
        return {'message': 'Product deleted successfully'}, 200
    
    @staticmethod
    def toggle_product_status(product_id):
        """Ẩn/hiện sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        new_status = ProductService.toggle_product_status(product_id)
        
        return {
            'message': f'Product {"activated" if new_status else "deactivated"} successfully',
            'product': product.to_dict()
        }, 200
    
    @staticmethod
    def update_stock(product_id, stock):
        """Cập nhật tồn kho"""
        if stock < 0:
            return {'error': 'Stock must be non-negative'}, 400
        
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        ProductService.update_stock(product_id, stock)
        
        logger.info(f"Stock updated for product {product_id}: {stock}")
        
        return {
            'message': 'Stock updated successfully',
            'product': product.to_dict()
        }, 200
    
    # === Image Management ===
    
    @staticmethod
    def upload_image(product_id, image_file, is_primary=False):
        """Upload ảnh sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Upload to Cloudinary
        image_url = CloudinaryService.upload_image(image_file, folder='products')
        
        if not image_url:
            return {'error': 'Failed to upload image'}, 500
        
        # Nếu là ảnh chính, cập nhật product.image_url
        if is_primary:
            ProductService.update_product(product_id, {'image_url': image_url})
        
        # Thêm vào bảng product_images
        product_image = ProductService.add_product_image(product_id, image_url, is_primary)
        
        logger.info(f"Image uploaded for product {product_id}")
        
        return {
            'message': 'Image uploaded successfully',
            'image': product_image.to_dict()
        }, 201
    
    @staticmethod
    def delete_image(product_id, image_id):
        """Xóa ảnh sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        image = ProductService.get_product_image(image_id)
        
        if not image or image.product_id != product_id:
            return {'error': 'Image not found'}, 404
        
        # Xóa trên Cloudinary
        CloudinaryService.delete_image_from_url(image.image_url)
        
        # Xóa trong database
        ProductService.delete_product_image(image_id)
        
        logger.info(f"Image deleted: {image_id}")
        
        return {'message': 'Image deleted successfully'}, 200
    
    # === Variant Management ===
    
    @staticmethod
    def create_variant(product_id, data):
        """Tạo biến thể sản phẩm"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'error': 'Product not found'}, 404
        
        # Check SKU uniqueness
        if ProductService.get_variant_by_sku(data['sku']):
            return {'error': 'Variant SKU already exists'}, 400
        
        variant = ProductService.create_variant(product_id, data)
        
        logger.info(f"Variant created for product {product_id}: {variant.id}")
        
        return {
            'message': 'Variant created successfully',
            'variant': variant.to_dict()
        }, 201
    
    @staticmethod
    def update_variant(product_id, variant_id, data):
        """Cập nhật biến thể"""
        variant = ProductService.get_variant_by_id(variant_id)
        
        if not variant or variant.product_id != product_id:
            return {'error': 'Variant not found'}, 404
        
        # Check SKU uniqueness if changed
        if 'sku' in data and data['sku'] != variant.sku:
            existing = ProductService.get_variant_by_sku(data['sku'])
            if existing:
                return {'error': 'Variant SKU already exists'}, 400
        
        updated_variant = ProductService.update_variant(variant_id, data)
        
        logger.info(f"Variant updated: {variant_id}")
        
        return {
            'message': 'Variant updated successfully',
            'variant': updated_variant.to_dict()
        }, 200
    
    @staticmethod
    def delete_variant(product_id, variant_id):
        """Xóa biến thể"""
        variant = ProductService.get_variant_by_id(variant_id)
        
        if not variant or variant.product_id != product_id:
            return {'error': 'Variant not found'}, 404
        
        ProductService.delete_variant(variant_id)
        
        logger.info(f"Variant deleted: {variant_id}")
        
        return {'message': 'Variant deleted successfully'}, 200
