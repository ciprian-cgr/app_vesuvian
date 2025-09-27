"""
API dependencies for dependency injection.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.users import UserRepository, UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Get user service instance wired with repository implementation."""
    repository = UserRepository(db)
    return UserService(repository)
