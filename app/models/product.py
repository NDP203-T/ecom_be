from datetime import datetime
from app import db
import uuid

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=True)  # Stock Keeping Unit
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))  # Ảnh chính
    category = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_images=False, include_variants=False):
        data = {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'image_url': self.image_url,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_images:
            data['images'] = [img.to_dict() for img in self.images]
        
        if include_variants:
            data['variants'] = [variant.to_dict() for variant in self.variants]
        
        return data


class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'image_url': self.image_url,
            'is_primary': self.is_primary,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat()
        }


class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)  # VD: "Đỏ - Size M"
    
    # Attributes
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    
    # Pricing & Stock
    price = db.Column(db.Numeric(10, 2))  # Null = dùng giá gốc
    stock = db.Column(db.Integer, default=0)
    
    # Image
    image_url = db.Column(db.String(500))
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'sku': self.sku,
            'name': self.name,
            'color': self.color,
            'size': self.size,
            'price': float(self.price) if self.price else None,
            'stock': self.stock,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
