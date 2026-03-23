from datetime import datetime
from app import db
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = db.Column(db.String(20), unique=True, nullable=False)  # ORD-20240101-0001
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Thông tin giao hàng
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120))
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(100))
    shipping_district = db.Column(db.String(100))
    shipping_ward = db.Column(db.String(100))
    
    # Thanh toán
    payment_method = db.Column(db.String(50), default='cash')  # cash, bank_transfer, credit_card
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, failed
    
    # Giá
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)  # Tổng tiền hàng
    shipping_fee = db.Column(db.Numeric(10, 2), default=0)  # Phí ship
    discount = db.Column(db.Numeric(10, 2), default=0)  # Giảm giá
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)  # Tổng thanh toán
    
    # Trạng thái đơn hàng
    status = db.Column(db.String(50), default='pending')  
    # pending, confirmed, processing, shipping, delivered, completed, cancelled
    
    # Ghi chú
    note = db.Column(db.Text)
    admin_note = db.Column(db.Text)  # Ghi chú nội bộ
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='orders')
    
    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'user_id': self.user_id,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_district': self.shipping_district,
            'shipping_ward': self.shipping_ward,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'subtotal': float(self.subtotal),
            'shipping_fee': float(self.shipping_fee),
            'discount': float(self.discount),
            'total_amount': float(self.total_amount),
            'status': self.status,
            'note': self.note,
            'admin_note': self.admin_note,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
            data['items_count'] = len(self.items)
        
        return data

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    variant_id = db.Column(db.String(36), db.ForeignKey('product_variants.id'), nullable=True)
    
    product_name = db.Column(db.String(200), nullable=False)  # Lưu tên để tránh mất data khi xóa product
    variant_name = db.Column(db.String(200))  # VD: "Black - 256GB"
    sku = db.Column(db.String(100))
    
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Giá tại thời điểm đặt
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)  # quantity * price
    
    # Relationships
    product = db.relationship('Product')
    variant = db.relationship('ProductVariant')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'variant_id': self.variant_id,
            'product_name': self.product_name,
            'variant_name': self.variant_name,
            'sku': self.sku,
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.subtotal)
        }
