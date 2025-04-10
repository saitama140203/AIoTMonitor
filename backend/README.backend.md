# AIoT Monitor Backend

Hệ thống giám sát thiết bị IoT thông minh dành cho môi trường nhà thông minh và nhà máy thông minh.

## Cài đặt và chạy với Docker

### Yêu cầu
- Docker & Docker Compose
- Git

### Các bước cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd aiot-monitor
```

2. Khởi động và build các containers:

```bash
docker-compose up --build
```
Nếu dùng docker v2 thì (loại bỏ -): 
```bash
docker compose up --build
```

3. Xem logs:
```bash
docker-compose logs -f api
```

### Truy cập các dịch vụ

- **API và Swagger UI**: http://localhost:8000/docs
- **PgAdmin**: http://localhost:5050
  - Email: admin@aiotmonitor.com
  - Password: admin123

### Tài khoản mặc định

Sau khi khởi động, hệ thống sẽ tạo tài khoản admin mặc định:
- **Username**: admin
- **Password**: admin123
- **Email**: admin@aiotmonitor.com

## Sử dụng API

### Đăng nhập và lấy token

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=admin&password=admin123'
```

### Tạo người dùng mới (yêu cầu quyền admin)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/auth/create-operator' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "operator1",
  "email": "operator1@example.com",
  "full_name": "Operator One",
  "password": "password123"
}'
```

## Quản lý database với Alembic

### Tạo migration mới
```bash
docker-compose exec api alembic revision --autogenerate -m "Mô tả thay đổi"
```

### Áp dụng migration
```bash
docker-compose exec api alembic upgrade head
```

## Các lệnh Docker thông dụng

### Khởi động containers
```bash
docker-compose up -d
```

### Dừng containers
```bash
docker-compose down
```

### Xem logs
```bash
docker-compose logs -f
```

### Xem trạng thái containers
```bash
docker-compose ps
```

### Kết nối vào PostgreSQL
```bash
docker-compose exec postgres psql -U postgres -d aiot_monitor
```

### Khởi động lại API service
```bash
docker-compose restart api
```