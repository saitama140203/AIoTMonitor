#!/bin/bash
set -e

echo "🕐 Đợi Postgres sẵn sàng..."
sleep 5

echo "🧩 Thực hiện Alembic migrations..."
cd app
alembic upgrade head
cd ..

echo "🚀 Khởi chạy FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload



echo ""
echo "==================================="
echo "API đang chạy tại: http://localhost:8000"
echo "Swagger UI: http://localhost:8000/docs"
echo "PgAdmin: http://localhost:5050"
echo "  - Email: admin@aiotmonitor.com"
echo "  - Password: admin123"
echo ""
echo "Tài khoản Admin mặc định:"
echo "  - Username: admin"
echo "  - Password: admin123"
echo "==================================="

# Hiển thị logs
docker-compose logs -f api