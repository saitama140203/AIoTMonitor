from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    group_id = Column(Integer, ForeignKey("groups.id"))  # Thêm khóa ngoại

    # Relationships
    group = relationship("Group", back_populates="profiles")  # Mỗi profile thuộc 1 group
    command_profiles = relationship("CommandProfile", back_populates="profile")
    profile_users = relationship("ProfileUser", back_populates="profile")

class ProfileUser(Base):
    __tablename__ = "profile_user"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    operator_id = Column(Integer, ForeignKey("users.id"))

    profile = relationship("Profile", back_populates="profile_users")
    user = relationship("User")
