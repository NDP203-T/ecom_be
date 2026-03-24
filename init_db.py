"""
Script để khởi tạo database và chạy migrations
"""
from app import create_app, db
from flask_migrate import init, migrate, upgrade
import os

def seed_sample_data():
    """Seed dữ liệu mẫu: categories và products"""
    from app.models.category import Category
    from app.models.product import Product, ProductVariant, ProductImage
    
    # Check nếu đã có data thì skip
    if Category.query.first() or Product.query.first():
        print("ℹ️  Sample data already exists, skipping seed...")
        return
    
    print("📦 Seeding sample data...")
    
    # 1. CATEGORIES
    electronics = Category(
        name='Electronics',
        slug='electronics',
        description='Electronic devices and gadgets',
        sort_order=1
    )
    db.session.add(electronics)
    db.session.flush()  # Get ID
    
    # Sub-categories
    categories_data = [
        {'name': 'Smartphones', 'slug': 'smartphones', 'parent_id': electronics.id, 'sort_order': 1},
        {'name': 'Laptops', 'slug': 'laptops', 'parent_id': electronics.id, 'sort_order': 2},
        {'name': 'Audio', 'slug': 'audio', 'parent_id': electronics.id, 'sort_order': 3},
        {'name': 'Tablets', 'slug': 'tablets', 'parent_id': electronics.id, 'sort_order': 4},
        {'name': 'Smartwatches', 'slug': 'smartwatches', 'parent_id': electronics.id, 'sort_order': 5},
        {'name': 'Cameras', 'slug': 'cameras', 'parent_id': electronics.id, 'sort_order': 6},
    ]
    
    for cat_data in categories_data:
        cat = Category(**cat_data)
        db.session.add(cat)
    
    db.session.commit()
    print("✅ Categories seeded!")
    
    # 2. PRODUCTS
    products_data = [
        # Smartphones
        {
            'name': 'iPhone 15 Pro Max',
            'sku': 'IP15PM-256',
            'description': 'Latest iPhone with A17 Pro chip, titanium design',
            'price': 1199.99,
            'stock': 50,
            'category': 'Smartphones',
            'variants': [
                {'sku': 'IP15PM-256-BLK', 'name': 'Black Titanium - 256GB', 'color': 'Black', 'size': '256GB', 'price': 1199.99, 'stock': 20},
                {'sku': 'IP15PM-512-BLU', 'name': 'Blue Titanium - 512GB', 'color': 'Blue', 'size': '512GB', 'price': 1399.99, 'stock': 15},
            ]
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'sku': 'SGS24U-256',
            'description': 'Flagship Samsung with S Pen, 200MP camera',
            'price': 1299.99,
            'stock': 40,
            'category': 'Smartphones',
            'variants': [
                {'sku': 'SGS24U-256-GRY', 'name': 'Titanium Gray - 256GB', 'color': 'Gray', 'size': '256GB', 'price': 1299.99, 'stock': 20},
                {'sku': 'SGS24U-512-BLK', 'name': 'Titanium Black - 512GB', 'color': 'Black', 'size': '512GB', 'price': 1499.99, 'stock': 20},
            ]
        },
        # Laptops
        {
            'name': 'MacBook Pro 16" M3 Max',
            'sku': 'MBP16-M3MAX',
            'description': 'Professional laptop with M3 Max chip',
            'price': 3499.99,
            'stock': 25,
            'category': 'Laptops',
            'variants': [
                {'sku': 'MBP16-M3MAX-36-1TB', 'name': '36GB RAM - 1TB SSD', 'size': '36GB/1TB', 'price': 3499.99, 'stock': 15},
                {'sku': 'MBP16-M3MAX-48-2TB', 'name': '48GB RAM - 2TB SSD', 'size': '48GB/2TB', 'price': 4299.99, 'stock': 10},
            ]
        },
        {
            'name': 'Dell XPS 15',
            'sku': 'DXPS15-I9',
            'description': 'Premium Windows laptop with Intel i9',
            'price': 2499.99,
            'stock': 30,
            'category': 'Laptops',
        },
        # Audio
        {
            'name': 'AirPods Pro 2',
            'sku': 'APP2-USB-C',
            'description': 'Active noise cancellation, USB-C charging',
            'price': 249.99,
            'stock': 100,
            'category': 'Audio',
        },
        {
            'name': 'Sony WH-1000XM5',
            'sku': 'SONY-WH1000XM5',
            'description': 'Industry-leading noise cancellation headphones',
            'price': 399.99,
            'stock': 60,
            'category': 'Audio',
            'variants': [
                {'sku': 'SONY-WH1000XM5-BLK', 'name': 'Black', 'color': 'Black', 'price': 399.99, 'stock': 30},
                {'sku': 'SONY-WH1000XM5-SLV', 'name': 'Silver', 'color': 'Silver', 'price': 399.99, 'stock': 30},
            ]
        },
        # Tablets
        {
            'name': 'iPad Pro 12.9" M2',
            'sku': 'IPADPRO-129-M2',
            'description': 'Professional tablet with M2 chip',
            'price': 1099.99,
            'stock': 35,
            'category': 'Tablets',
            'variants': [
                {'sku': 'IPADPRO-129-256-WIFI', 'name': '256GB WiFi', 'size': '256GB WiFi', 'price': 1099.99, 'stock': 20},
                {'sku': 'IPADPRO-129-512-CELL', 'name': '512GB Cellular', 'size': '512GB Cellular', 'price': 1499.99, 'stock': 15},
            ]
        },
        # Smartwatches
        {
            'name': 'Apple Watch Ultra 2',
            'sku': 'AWU2-49MM',
            'description': 'Rugged smartwatch for extreme conditions',
            'price': 799.99,
            'stock': 45,
            'category': 'Smartwatches',
        },
        {
            'name': 'Samsung Galaxy Watch 6',
            'sku': 'SGW6-44MM',
            'description': 'Advanced health tracking smartwatch',
            'price': 349.99,
            'stock': 55,
            'category': 'Smartwatches',
            'variants': [
                {'sku': 'SGW6-44-BLK', 'name': 'Black - 44mm', 'color': 'Black', 'size': '44mm', 'price': 349.99, 'stock': 30},
                {'sku': 'SGW6-40-SLV', 'name': 'Silver - 40mm', 'color': 'Silver', 'size': '40mm', 'price': 329.99, 'stock': 25},
            ]
        },
        # Cameras
        {
            'name': 'Sony A7 IV',
            'sku': 'SONY-A7IV-BODY',
            'description': 'Professional mirrorless camera body',
            'price': 2499.99,
            'stock': 20,
            'category': 'Cameras',
        },
        {
            'name': 'Canon EOS R6 Mark II',
            'sku': 'CANON-R6M2-BODY',
            'description': 'High-performance mirrorless camera',
            'price': 2399.99,
            'stock': 18,
            'category': 'Cameras',
        },
    ]
    
    for prod_data in products_data:
        variants_data = prod_data.pop('variants', [])
        
        product = Product(**prod_data)
        db.session.add(product)
        db.session.flush()
        
        # Add variants
        for var_data in variants_data:
            var_data['product_id'] = product.id
            variant = ProductVariant(**var_data)
            db.session.add(variant)
    
    db.session.commit()
    print("✅ Products seeded!")
    print(f"   Total: {len(products_data)} products")

def init_database():
    app = create_app()
    
    with app.app_context():
        # Tạo tất cả tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Import models để đảm bảo được load
        from app.models import User, OTP, Product, Order, OrderItem
        print("✅ Models loaded successfully!")
        
        # Tạo admin mặc định
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@ecommerce.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@123456')
        
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if not existing_admin:
            admin = User(
                email=admin_email,
                full_name='System Admin',
                role='admin',
                is_verified=True,
                is_active=True
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ Admin account created!")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            print(f"   ⚠️  CHANGE PASSWORD AFTER FIRST LOGIN!")
        else:
            print(f"ℹ️  Admin account already exists: {admin_email}")
        
        # Seed sample data
        seed_sample_data()

if __name__ == '__main__':
    init_database()
