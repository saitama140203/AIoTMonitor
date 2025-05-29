from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    status = Column(Enum("active", "terminated", name="session_status"), nullable=False, default="active")
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    current_command = Column(String(255))
    connected_time = Column(DateTime(timezone=True))  

    # Relationships
    operator = relationship("User", back_populates="sessions")
    device = relationship("Device")
    session_history = relationship("SessionHistory", back_populates="session", cascade="all, delete-orphan")
    commands = relationship("SessionCommand", back_populates="session", cascade="all, delete-orphan")

class SessionHistory(Base):
    __tablename__ = "session_history"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    terminated_by = Column(Integer, ForeignKey("users.id"))
    connected_time = Column(DateTime(timezone=True))
    end_status = Column(String(50))  # e.g., "completed", "killed", "failed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    history_text = Column(String) 
    
    # Relationships
    session = relationship("Session", back_populates="session_history")
    terminator = relationship("User", back_populates="terminated_sessions", foreign_keys=[terminated_by])

class SessionCommand(Base):
    __tablename__ = "session_commands"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, index=True)
    command_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("Session", back_populates="commands")
