# E-Commerce Flask API

Dự án e-commerce API sử dụng Flask, PostgreSQL, Redis, Cloudinary và Docker.

## Tính năng

- Xác thực người dùng (JWT)
- Quản lý sản phẩm (CRUD)
- Giỏ hàng (Redis cache)
- Đặt hàng
- Upload ảnh sản phẩm (Cloudinary)

## Cài đặt

1. Copy file cấu hình:
```bash
cp .env.example .env
```

2. Cập nhật thông tin Cloudinary trong file `.env`

3. Chạy với Docker:
```bash
docker-compose up -d
```

4. Tạo database tables:
```bash
docker-compose exec app flask db init
docker-compose exec app flask db migrate
docker-compose exec app flask db upgrade
```

## API Endpoints

### Auth
- POST `/api/auth/register` - Đăng ký
- POST `/api/auth/login` - Đăng nhập
- GET `/api/auth/me` - Thông tin user (cần JWT)

### Products
- GET `/api/products` - Danh sách sản phẩm
- GET `/api/products/<id>` - Chi tiết sản phẩm
- POST `/api/products` - Tạo sản phẩm (cần JWT)

### Cart
- GET `/api/cart` - Xem giỏ hàng (cần JWT)
- POST `/api/cart/add` - Thêm vào giỏ (cần JWT)
- DELETE `/api/cart/remove/<id>` - Xóa khỏi giỏ (cần JWT)

### Orders
- POST `/api/orders` - Tạo đơn hàng (cần JWT)
- GET `/api/orders` - Danh sách đơn hàng (cần JWT)

## Tech Stack

- Flask
- PostgreSQL
- Redis
- Cloudinary
- Docker
