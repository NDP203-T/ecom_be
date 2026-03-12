#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."

# Đợi PostgreSQL sẵn sàng
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "postgres" -U "ecom_user" -d "ecom_db" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is up - initializing database"

# Khởi tạo database
python init_db.py

echo "Starting Flask application..."

# Chạy Flask app
exec "$@"
