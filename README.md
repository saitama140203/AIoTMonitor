# AIoT Monitor

AIoT Monitor là một hệ thống giám sát và quản lý thiết bị IoT thông minh, cung cấp giải pháp trung gian giữa nhân viên vận hành và các thiết bị hub, giúp đảm bảo ổn định cho các giải pháp smart house và smart factory.

## Tổng quan

Hệ thống AIoT Monitor được phát triển để giải quyết các vấn đề trong quá trình giám sát thiết bị IoT:
- Giám sát việc tuân thủ lịch trình kiểm tra của nhân viên
- Ghi log toàn bộ hoạt động và các lệnh thực thi
- Phát hiện hành vi bất thường và cảnh báo kịp thời
- Đảm bảo tính ổn định của hệ thống IoT

## Kiến trúc hệ thống

### Backend (FastAPI)
- REST API cho tương tác với frontend và các service khác
- Xác thực và phân quyền (RBAC)
- Kết nối và quản lý nhiều loại CSDL (PostgreSQL, InfluxDB, Elasticsearch)
- Business logic cho các nghiệp vụ

### Frontend (Vue.js)
- Giao diện quản trị
- Dashboard theo dõi trạng thái hệ thống
- Console kết nối đến hub
- Báo cáo và thống kê

### AI
- Phát hiện anomaly trong hành vi người dùng
- Phân tích lệnh để xác định rủi ro
- Nhận diện mẫu hành vi và phát hiện bất thường

### Connection Proxy
- Trung gian hóa kết nối giữa nhân viên và hub
- Hỗ trợ nhiều giao thức (SSH, VNC, RDP)
- Ghi log toàn bộ lệnh và hoạt động

### Cơ sở dữ liệu
- PostgreSQL: Lưu trữ dữ liệu người dùng, cấu hình và metadata
- InfluxDB: Lưu trữ dữ liệu time-series từ thiết bị IoT
- Elasticsearch: Lưu trữ và phân tích log

## Tính năng chính


## Công nghệ sử dụng

- **Backend**: FastAPI (Python)
- **Frontend**: Vue.js 3 (JavaScript)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL, InfluxDB, Elasticsearch
- **AI**: Scikit-learn, PyTorch
- **Connection**: Apache Guacamole
- **Authentication**: JWT, OAuth2
- **Containerization**: Docker & Kubernetes

## Cài đặt và chạy

### Yêu cầu
- Docker & Docker Compose
- Python 3.9+
- Node.js 16+

### Backend

```bash
# Clone repository
git clone https://github.com/your-org/aiot-monitor.git
cd aiot-monitor/backend

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy migrations
alembic upgrade head

# Chạy server
uvicorn app.main:app --reload
```

### Frontend

```bash
# Di chuyển đến thư mục frontend
cd ../frontend

# Cài đặt dependencies
pass

# Chạy server development
pass

# Build cho production
pass
```

### Docker Compose

```bash
# Chạy toàn bộ hệ thống
docker-compose up -d
```

## API Documentation

API documentation được tự động tạo bởi FastAPI và có thể truy cập tại:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Cấu trúc thư mục

```
aiot-monitor/
├── backend/             # Backend API với FastAPI
├── frontend/            # Frontend với Vue.js
└── ai/                  # Các module AI
```

## Phát triển

### Setup môi trường development

1. Clone repository
2. Tạo và kích hoạt môi trường ảo Python
3. Cài đặt dependencies cho backend
4. Cài đặt dependencies cho frontend
5. Cấu hình file .env theo .env.example

### Conventions

- **Code Style**: Backend tuân theo PEP 8, Frontend tuân theo ESLint config
- **Git Workflow**: Feature branches, Pull requests, Code reviews
- **Tests**: Viết unit tests và integration tests cho các tính năng mới

## License

Dự án này được phân phối dưới giấy phép [MIT License](LICENSE).

## Tài liệu tham khảo

- [Apache Guacamole](https://github.com/apache/guacamole-server)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)

## Liên hệ

Nếu có bất kỳ câu hỏi hoặc đề xuất nào, vui lòng mở một issue trên GitHub hoặc liên hệ với team phát triển.
