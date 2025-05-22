# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    roles = relationship("UserRole", back_populates="user")
    devices = relationship("Device", back_populates="creator")
    commands = relationship("Command", back_populates="creator")
    activity_logs = relationship("ActivityLog", back_populates="user")
    sessions = relationship("Session", back_populates="operator", cascade="all, delete-orphan")
    terminated_sessions = relationship("SessionHistory", back_populates="terminator", foreign_keys='SessionHistory.terminated_by', cascade="all, delete-orphan")

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255))
    
    users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_role"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")