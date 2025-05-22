from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import session as session_models  # Import models session

# Khởi tạo engine với cấu hình từ settings
print("Creating database engine with URI:", settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Kiểm tra kết nối trước khi sử dụng
    connect_args={"check_same_thread": False} if "sqlite" in settings.SQLALCHEMY_DATABASE_URI else {}
)

# Tạo session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Tạo bảng cho các models session (nếu chưa tồn tại)
def init_db():
    session_models.Base.metadata.create_all(bind=engine)
    print("Initialized database tables for session models")

# Gọi hàm khởi tạo khi import module
init_db()