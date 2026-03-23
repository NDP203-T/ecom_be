from app import db
from app.models.product import Product, ProductImage, ProductVariant

class ProductService:
    
    # === Product CRUD ===
    
    @staticmethod
    def get_all_products(page=1, per_page=20, category=None, is_active=None):
        """Lấy danh sách sản phẩm với filter"""
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true' if isinstance(is_active, str) else is_active
            query = query.filter_by(is_active=is_active_bool)
        
        pagination = query.order_by(Product.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return pagination.items, pagination.total
    
    @staticmethod
    def get_product_by_id(product_id):
        """Lấy sản phẩm theo ID"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_product_by_sku(sku):
        """Lấy sản phẩm theo SKU"""
        return Product.query.filter_by(sku=sku).first()
    
    @staticmethod
    def create_product(data):
        """Tạo sản phẩm mới"""
        product = Product(
            name=data['name'],
            sku=data.get('sku'),
            description=data.get('description'),
            price=data['price'],
            stock=data.get('stock', 0),
            image_url=data.get('image_url'),
            category=data.get('category'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product
    
    @staticmethod
    def update_product(product_id, data):
        """Cập nhật sản phẩm"""
        product = Product.query.get(product_id)
        
        if product:
            for key, value in data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            
            db.session.commit()
        
        return product
    
    @staticmethod
    def delete_product(product_id):
        """Xóa sản phẩm"""
        product = Product.query.get(product_id)
        
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def toggle_product_status(product_id):
        """Ẩn/hiện sản phẩm"""
        product = Product.query.get(product_id)
        
        if product:
            product.is_active = not product.is_active
            db.session.commit()
            return product.is_active
        
        return None
    
    @staticmethod
    def update_stock(product_id, stock):
        """Cập nhật tồn kho"""
        product = Product.query.get(product_id)
        
        if product:
            product.stock = stock
            db.session.commit()
            return product
        
        return None
    
    # === Product Images ===
    
    @staticmethod
    def add_product_image(product_id, image_url, is_primary=False):
        """Thêm ảnh cho sản phẩm"""
        # Nếu là ảnh chính, set các ảnh khác thành không phải ảnh chính
        if is_primary:
            ProductImage.query.filter_by(product_id=product_id).update({'is_primary': False})
        
        # Lấy sort_order cao nhất
        max_order = db.session.query(db.func.max(ProductImage.sort_order)).filter_by(
            product_id=product_id
        ).scalar() or 0
        
        image = ProductImage(
            product_id=product_id,
            image_url=image_url,
            is_primary=is_primary,
            sort_order=max_order + 1
        )
        
        db.session.add(image)
        db.session.commit()
        
        return image
    
    @staticmethod
    def get_product_image(image_id):
        """Lấy ảnh theo ID"""
        return ProductImage.query.get(image_id)
    
    @staticmethod
    def delete_product_image(image_id):
        """Xóa ảnh sản phẩm"""
        image = ProductImage.query.get(image_id)
        
        if image:
            db.session.delete(image)
            db.session.commit()
            return True
        
        return False
    
    # === Product Variants ===
    
    @staticmethod
    def create_variant(product_id, data):
        """Tạo biến thể sản phẩm"""
        variant = ProductVariant(
            product_id=product_id,
            sku=data['sku'],
            name=data['name'],
            color=data.get('color'),
            size=data.get('size'),
            price=data.get('price'),
            stock=data.get('stock', 0),
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(variant)
        db.session.commit()
        
        return variant
    
    @staticmethod
    def get_variant_by_id(variant_id):
        """Lấy biến thể theo ID"""
        return ProductVariant.query.get(variant_id)
    
    @staticmethod
    def get_variant_by_sku(sku):
        """Lấy biến thể theo SKU"""
        return ProductVariant.query.filter_by(sku=sku).first()
    
    @staticmethod
    def update_variant(variant_id, data):
        """Cập nhật biến thể"""
        variant = ProductVariant.query.get(variant_id)
        
        if variant:
            for key, value in data.items():
                if hasattr(variant, key):
                    setattr(variant, key, value)
            
            db.session.commit()
        
        return variant
    
    @staticmethod
    def delete_variant(variant_id):
        """Xóa biến thể"""
        variant = ProductVariant.query.get(variant_id)
        
        if variant:
            db.session.delete(variant)
            db.session.commit()
            return True
        
        return False
