"""
User service layer with business logic.
"""
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.logging import LoggerMixin


class UserService(LoggerMixin):
    """User service with business logic."""
    
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = await self.repository.get_by_username(user_create.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user
        user_data = user_create.dict()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        return await self.repository.create(user_data)
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await self.repository.get_by_id(user_id)
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user."""
        user_data = user_update.dict(exclude_unset=True)
        
        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
        
        return await self.repository.update(user_id, user_data)
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return await self.repository.delete(user_id)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        user = await self.repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
