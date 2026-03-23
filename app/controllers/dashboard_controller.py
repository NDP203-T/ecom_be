from datetime import datetime, timedelta
from app.services.dashboard_service import DashboardService

class DashboardController:
    
    @staticmethod
    def get_overview():
        """Lấy tổng quan dashboard"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Tổng doanh thu
        total_revenue = DashboardService.get_total_revenue()
        
        # Doanh thu hôm nay
        today_revenue = DashboardService.get_total_revenue(
            start_date=today
        )
        
        # Số đơn hàng hôm nay
        today_orders = DashboardService.get_orders_count(
            start_date=today
        )
        
        # Tổng số đơn hàng
        total_orders = DashboardService.get_orders_count()
        
        # Số người dùng
        total_users = DashboardService.get_users_count()
        
        # Sản phẩm bán chạy
        top_products = DashboardService.get_top_selling_products(limit=5)
        
        # Biểu đồ doanh thu 7 ngày
        revenue_chart = DashboardService.get_revenue_chart(period='day', days=7)
        
        return {
            'overview': {
                'total_revenue': total_revenue,
                'today_revenue': today_revenue,
                'today_orders': today_orders,
                'total_orders': total_orders,
                'total_users': total_users
            },
            'top_products': top_products,
            'revenue_chart': revenue_chart
        }, 200
