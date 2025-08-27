# backend/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_instructor = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # relationships
    submissions = relationship("Submission", back_populates="user")
    progress = relationship("Progress", back_populates="user")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course = Column(String, nullable=False)
    content = Column(Text)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="submissions")

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course = Column(String, nullable=False)
    percent = Column(Float, default=0.0)
    last_update = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="progress")
