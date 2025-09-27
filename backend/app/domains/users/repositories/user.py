"""
User repository implementation with user-specific operations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.users.models.user import User
from app.core.base_repository import BaseRepository


class IUserRepository(ABC):
    """Abstract interface for user repository operations."""

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> User:
        ...

    @abstractmethod
    async def update(self, id: str, obj_in: dict) -> Optional[User]:
        ...

    @abstractmethod
    async def delete(self, id: str) -> bool:
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        ...


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
