# app/models/command.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    commands_text = Column(String)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    creator = relationship("User", back_populates="commands")
    command_profiles = relationship("CommandProfile", back_populates="command")

class CommandProfile(Base):
    __tablename__ = "command_profile"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    command_id = Column(Integer, ForeignKey("commands.id"))

    profile = relationship("Profile", back_populates="command_profiles")
    command = relationship("Command", back_populates="command_profiles")