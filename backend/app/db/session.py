
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

print("Creating database engine with URI:", settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)