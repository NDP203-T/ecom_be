from datetime import datetime, timedelta
from sqlalchemy import func, desc
from app import db
from app.models import User, Order, OrderItem, Product

class DashboardService:
    
    @staticmethod
    def get_total_revenue(start_date=None, end_date=None):
        """Tính tổng doanh thu"""
        query = db.session.query(func.sum(Order.total_amount)).filter(
            Order.status == 'completed'
        )
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        result = query.scalar()
        return float(result) if result else 0.0
    
    @staticmethod
    def get_orders_count(start_date=None, end_date=None):
        """Đếm số đơn hàng"""
        query = Order.query
        
        if start_date:
            query = query.filter(Order.created_at >= start_date)
        if end_date:
            query = query.filter(Order.created_at <= end_date)
        
        return query.count()
    
    @staticmethod
    def get_users_count():
        """Đếm số người dùng"""
        return User.query.filter_by(is_verified=True).count()
    
    @staticmethod
    def get_top_selling_products(limit=5):
        """Lấy sản phẩm bán chạy"""
        result = db.session.query(
            Product.id,
            Product.name,
            Product.image_url,
            Product.price,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(OrderItem).join(Order).filter(
            Order.status == 'completed'
        ).group_by(
            Product.id, Product.name, Product.image_url, Product.price
        ).order_by(
            desc('total_sold')
        ).limit(limit).all()
        
        return [{
            'id': r.id,
            'name': r.name,
            'image_url': r.image_url,
            'price': float(r.price),
            'total_sold': r.total_sold
        } for r in result]
    
    @staticmethod
    def get_revenue_chart(period='day', days=7):
        """Lấy dữ liệu biểu đồ doanh thu"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        if period == 'day':
            # Group by day
            result = db.session.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total_amount).label('revenue')
            ).filter(
                Order.status == 'completed',
                Order.created_at >= start_date
            ).group_by(
                func.date(Order.created_at)
            ).order_by('date').all()
            
            return [{
                'date': r.date.isoformat(),
                'revenue': float(r.revenue) if r.revenue else 0.0
            } for r in result]
        
        return []
