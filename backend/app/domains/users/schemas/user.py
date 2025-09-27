"""
User Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """User schema with database fields."""
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    refresh_token_version: int = 0
    
    # Pydantic v2+ config
    model_config = ConfigDict(from_attributes=True)


class User(UserInDB):
    """Public user schema."""
    pass


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""
    user_id: Optional[str] = None
