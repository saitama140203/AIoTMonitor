from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    mac = Column(String(50))
    ip = Column(String(50))
    status = Column(String(20))  # Ví dụ: 'active', 'inactive', 'maintenance'
    platform = Column(String(100))
    lastseen = Column(DateTime)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    group = relationship("Group", back_populates="devices")
    creator = relationship("User", back_populates="devices")
    activity_logs = relationship("ActivityLog", back_populates="device")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_actived = Column(Boolean, default=True)

    devices = relationship("Device", back_populates="group")
    profiles = relationship("Profile", back_populates="group")
