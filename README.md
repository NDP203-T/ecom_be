# E-Commerce Flask API

Dự án e-commerce API sử dụng Flask, PostgreSQL, Cloudinary và Docker.

## Tính năng

- Xác thực người dùng (JWT)
- Quản lý sản phẩm (CRUD)
- Giỏ hàng
- Đặt hàng
- Upload ảnh sản phẩm (Cloudinary)

## Default Admin Account

Khi khởi động lần đầu, hệ thống tự động tạo admin account:

```
Email: admin@ecommerce.com
Password: Admin@123456
```

**⚠️ QUAN TRỌNG:** Đổi password ngay sau lần đăng nhập đầu tiên!

Để thay đổi admin mặc định, cập nhật trong `.env`:
```
ADMIN_EMAIL=your-admin@email.com
ADMIN_PASSWORD=YourSecurePassword
```

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

## API Documentation

Swagger UI: `http://localhost:5000/api/docs`

**Decrypt Helper:** `http://localhost:5000/decrypt`

Trang web để giải mã response từ Swagger. Chỉ cần:
1. Nhập SECRET_KEY
2. Copy/paste response từ Swagger
3. Click Decrypt

## Response Encryption

**Tất cả auth endpoints đều mã hóa response tự động.**

Response có dạng:
```json
{
  "encrypted": true,
  "data": "base64_encrypted_string..."
}
```

### Giải mã ở Frontend

**JavaScript (Browser):**
```javascript
// Xem file client-example.html
```

**Node.js:**
```javascript
// Xem file client-example.js
const { decryptData } = require('./client-example.js');

const response = await fetch('/api/auth/login', {...});
const result = await response.json();

if (result.encrypted) {
    const decrypted = decryptData(result.data);
    console.log(decrypted);
}
```

**Python:**
```python
from app.utils.encryption import EncryptionUtil

encrypted_data = response['data']
decrypted = EncryptionUtil.decrypt_data(encrypted_data)
```

Chi tiết xem [ENCRYPTION.md](ENCRYPTION.md)

## Database Management

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

