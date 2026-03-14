# E-Commerce Flask API

Dự án e-commerce API sử dụng Flask, PostgreSQL, Cloudinary và Docker.

## Tính năng

- Xác thực người dùng (JWT)
- Quản lý sản phẩm (CRUD)
- Giỏ hàng
- Đặt hàng
- Upload ảnh sản phẩm (Cloudinary)

## Cài đặt và chạy

### 1. Cấu hình môi trường

```bash
cp .env.example .env
```

Sửa file `.env` với thông tin của bạn (đặc biệt là Cloudinary credentials)

### 2. Chạy với Docker (Khuyến nghị)

```bash
# Khởi động Docker Desktop trước

# Build và chạy
docker-compose up -d

# Xem logs
docker-compose logs -f app
```

Database sẽ tự động được khởi tạo khi container start!

### 3. Chạy local (không dùng Docker)

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Khởi tạo database
python init_db.py

# Chạy app
python run.py
```

## Database Management

pgAdmin: `http://localhost:5050`
- Email: `admin@admin.com`
- Password: `admin`

Kết nối database trong pgAdmin:
- Host: `postgres` (hoặc `localhost` nếu kết nối từ máy local)
- Port: `5432`
- Database: `ecom_db`
- Username: `ecom_user`
- Password: `ecom_pass`

## API Documentation

Swagger UI: `http://localhost:5000/api/docs`

## API Endpoints

### Auth
- `POST /api/auth/register` - Đăng ký
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }
  ```

- `POST /api/auth/login` - Đăng nhập
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

## Tech Stack

- Flask 3.0
- PostgreSQL 15
- Cloudinary
- Docker & Docker Compose
- JWT Authentication

## Cấu trúc project

```
app/
├── controllers/     # Business logic
├── models/         # Database models
├── routes/         # API endpoints
├── services/       # Reusable services
├── middleware/     # Validation, security
└── swagger/        # API documentation
```

## Git Commit Convention
**Examples:**
```bash
git commit -m "feat: add user registration"
git commit -m "fix: resolve login validation error"
git commit -m "docs: update API documentation"
```

