"""
User model definition.
"""
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from uuid import uuid4
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """User model."""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # integer version used to invalidate/rotate refresh tokens
    refresh_token_version = Column(Integer, default=0, nullable=False)
