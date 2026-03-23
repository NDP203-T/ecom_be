from app import db
from app.models.order import Order, OrderItem
from app.models.product import Product, ProductVariant
from datetime import datetime

class OrderService:
    
    @staticmethod
    def generate_order_number():
        """Tạo mã đơn hàng: ORD-20240101-0001"""
        today = datetime.utcnow().strftime('%Y%m%d')
        
        # Đếm số đơn hàng trong ngày
        count = Order.query.filter(
            Order.order_number.like(f'ORD-{today}-%')
        ).count()
        
        return f'ORD-{today}-{str(count + 1).zfill(4)}'
    
    @staticmethod
    def create_order(user_id, data):
        """Tạo đơn hàng mới"""
        # Tạo order
        order = Order(
            order_number=OrderService.generate_order_number(),
            user_id=user_id,
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
            customer_email=data.get('customer_email'),
            shipping_address=data['shipping_address'],
            shipping_city=data.get('shipping_city'),
            shipping_district=data.get('shipping_district'),
            shipping_ward=data.get('shipping_ward'),
            payment_method=data.get('payment_method', 'cash'),
            shipping_fee=data.get('shipping_fee', 0),
            discount=data.get('discount', 0),
            note=data.get('note'),
            subtotal=0,
            total_amount=0
        )
        
        db.session.add(order)
        db.session.flush()  # Để có order.id
        
        # Thêm order items
        subtotal = 0
        for item_data in data['items']:
            product = Product.query.get(item_data['product_id'])
            if not product:
                raise ValueError(f"Product {item_data['product_id']} not found")
            
            # Check stock
            if product.stock < item_data['quantity']:
                raise ValueError(f"Insufficient stock for {product.name}")
            
            # Lấy giá và thông tin
            variant = None
            price = float(product.price)
            variant_name = None
            sku = product.sku
            
            if item_data.get('variant_id'):
                variant = ProductVariant.query.get(item_data['variant_id'])
                if variant:
                    if variant.price:
                        price = float(variant.price)
                    variant_name = variant.name
                    sku = variant.sku
                    
                    # Check variant stock
                    if variant.stock < item_data['quantity']:
                        raise ValueError(f"Insufficient stock for {variant.name}")
            
            item_subtotal = price * item_data['quantity']
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                variant_id=variant.id if variant else None,
                product_name=product.name,
                variant_name=variant_name,
                sku=sku,
                quantity=item_data['quantity'],
                price=price,
                subtotal=item_subtotal
            )
            
            db.session.add(order_item)
            subtotal += item_subtotal
            
            # Trừ stock
            if variant:
                variant.stock -= item_data['quantity']
            else:
                product.stock -= item_data['quantity']
        
        # Cập nhật tổng tiền
        order.subtotal = subtotal
        order.total_amount = subtotal + float(order.shipping_fee) - float(order.discount)
        
        db.session.commit()
        return order
    
    @staticmethod
    def get_order_by_id(order_id):
        """Lấy đơn hàng theo ID"""
        return Order.query.get(order_id)
    
    @staticmethod
    def get_order_by_number(order_number):
        """Lấy đơn hàng theo order_number"""
        return Order.query.filter_by(order_number=order_number).first()
    
    @staticmethod
    def get_user_orders(user_id, page=1, per_page=10):
        """Lấy đơn hàng của user"""
        pagination = Order.query.filter_by(user_id=user_id).order_by(
            Order.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return pagination.items, pagination.total
    
    @staticmethod
    def get_all_orders(page=1, per_page=20, status=None):
        """Lấy tất cả đơn hàng (Admin)"""
        query = Order.query
        
        if status:
            query = query.filter_by(status=status)
        
        pagination = query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return pagination.items, pagination.total
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Cập nhật trạng thái đơn hàng"""
        order = Order.query.get(order_id)
        
        if order:
            order.status = new_status
            
            # Cập nhật timestamp tương ứng
            if new_status == 'confirmed':
                order.confirmed_at = datetime.utcnow()
            elif new_status == 'delivered':
                order.delivered_at = datetime.utcnow()
                order.payment_status = 'paid'  # COD được thanh toán khi giao hàng
            elif new_status == 'completed':
                order.completed_at = datetime.utcnow()
                if not order.delivered_at:
                    order.delivered_at = datetime.utcnow()
                order.payment_status = 'paid'
            elif new_status == 'cancelled':
                order.cancelled_at = datetime.utcnow()
                # Hoàn lại stock
                OrderService.restore_stock(order)
            
            db.session.commit()
        
        return order
    
    @staticmethod
    def restore_stock(order):
        """Hoàn lại stock khi hủy đơn"""
        for item in order.items:
            if item.variant_id:
                variant = ProductVariant.query.get(item.variant_id)
                if variant:
                    variant.stock += item.quantity
            else:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock += item.quantity
        
        db.session.commit()
    
    @staticmethod
    def update_admin_note(order_id, note):
        """Cập nhật ghi chú admin"""
        order = Order.query.get(order_id)
        
        if order:
            order.admin_note = note
            db.session.commit()
        
        return order
    
    @staticmethod
    def cancel_order(order_id, user_id=None):
        """Hủy đơn hàng"""
        order = Order.query.get(order_id)
        
        if not order:
            return None
        
        # Nếu có user_id, check quyền sở hữu
        if user_id and order.user_id != user_id:
            return None
        
        # Chỉ cho phép hủy đơn pending hoặc confirmed
        if order.status not in ['pending', 'confirmed']:
            return None
        
        return OrderService.update_order_status(order_id, 'cancelled')
