from app.services.order_service import OrderService
import logging

logger = logging.getLogger(__name__)

class OrderController:
    
    @staticmethod
    def create_order(user_id, data):
        """Tạo đơn hàng mới"""
        # Validate items
        if not data.get('items') or len(data['items']) == 0:
            return {'error': 'Order must have at least one item'}, 400
        
        # Validate shipping info
        required_fields = ['customer_name', 'customer_phone', 'shipping_address']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field} is required'}, 400
        
        try:
            order = OrderService.create_order(user_id, data)
            
            logger.info(f"Order created: {order.order_number} by user {user_id}")
            
            return {
                'message': 'Order created successfully',
                'order': order.to_dict()
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating order: {str(e)}")
            return {'error': 'Failed to create order'}, 500
    
    @staticmethod
    def get_order_by_id(order_id, user_id=None):
        """Lấy chi tiết đơn hàng"""
        order = OrderService.get_order_by_id(order_id)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        # Nếu không phải admin, check quyền sở hữu
        if user_id and order.user_id != user_id:
            return {'error': 'Access denied'}, 403
        
        return {'order': order.to_dict()}, 200
    
    @staticmethod
    def get_order_by_number(order_number, user_id=None):
        """Lấy đơn hàng theo order_number"""
        order = OrderService.get_order_by_number(order_number)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        # Nếu không phải admin, check quyền sở hữu
        if user_id and order.user_id != user_id:
            return {'error': 'Access denied'}, 403
        
        return {'order': order.to_dict()}, 200
    
    @staticmethod
    def get_user_orders(user_id, page=1, per_page=10):
        """Lấy danh sách đơn hàng của user"""
        orders, total = OrderService.get_user_orders(user_id, page, per_page)
        
        return {
            'orders': [order.to_dict(include_items=False) for order in orders],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }, 200
    
    @staticmethod
    def get_all_orders(page=1, per_page=20, status=None):
        """Lấy tất cả đơn hàng (Admin)"""
        orders, total = OrderService.get_all_orders(page, per_page, status)
        
        return {
            'orders': [order.to_dict(include_items=False) for order in orders],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        }, 200
    
    @staticmethod
    def update_order_status(order_id, new_status):
        """Cập nhật trạng thái đơn hàng (Admin)"""
        valid_statuses = ['pending', 'confirmed', 'processing', 'shipping', 'delivered', 'completed', 'cancelled']
        
        if new_status not in valid_statuses:
            return {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}, 400
        
        order = OrderService.update_order_status(order_id, new_status)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        logger.info(f"Order {order.order_number} status updated to {new_status}")
        
        return {
            'message': f'Order status updated to {new_status}',
            'order': order.to_dict()
        }, 200
    
    @staticmethod
    def update_admin_note(order_id, note):
        """Cập nhật ghi chú admin"""
        order = OrderService.update_admin_note(order_id, note)
        
        if not order:
            return {'error': 'Order not found'}, 404
        
        return {
            'message': 'Admin note updated',
            'order': order.to_dict()
        }, 200
    
    @staticmethod
    def cancel_order(order_id, user_id=None):
        """Hủy đơn hàng"""
        order = OrderService.cancel_order(order_id, user_id)
        
        if not order:
            return {'error': 'Order not found or cannot be cancelled'}, 400
        
        logger.info(f"Order {order.order_number} cancelled")
        
        return {
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }, 200
