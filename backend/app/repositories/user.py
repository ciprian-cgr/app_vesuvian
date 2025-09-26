"""
User repository implementation with user-specific operations.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class IUserRepository(BaseRepository[User]):
    """Interface for user repository operations."""
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass


class UserRepository(BaseRepository[User], IUserRepository):
    """User repository implementation."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        try:
            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            self.logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        try:
            result = await self.db.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            self.logger.error(f"Error getting user by username {username}: {e}")
            return None
