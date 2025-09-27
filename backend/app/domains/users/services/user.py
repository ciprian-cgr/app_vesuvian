"""
User service layer with business logic.
"""
from typing import Optional, List

from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.domains.users.models.user import User
from app.domains.users.repositories.user import IUserRepository
from app.domains.users.schemas.user import UserCreate, UserUpdate
from app.core.logging import LoggerMixin


class UserService(LoggerMixin):
    """User service with business logic.

    This service depends on a repository implementing `IUserRepository`.
    """

    def __init__(self, repository: IUserRepository) -> None:
        self.repository = repository

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await self.repository.get_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        existing_username = await self.repository.get_by_username(user_create.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # Create user
        user_data = user_create.model_dump() if hasattr(user_create, "model_dump") else user_create.dict()
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

        return await self.repository.create(user_data)

    async def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return await self.repository.get_by_id(user_id)

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return await self.repository.get_all(skip=skip, limit=limit)

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        """Update user."""
        user_data = user_update.model_dump(exclude_unset=True) if hasattr(user_update, "model_dump") else user_update.dict(exclude_unset=True)

        if "password" in user_data:
            user_data["hashed_password"] = get_password_hash(user_data.pop("password"))

        return await self.repository.update(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        return await self.repository.delete(user_id)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password."""
        user = await self.repository.get_by_email(email)
        # user.hashed_password is an ORM-mapped attribute; mypy cannot statically
        # infer its runtime type here. Silence the type check.
        if not user or not verify_password(password, user.hashed_password):  # type: ignore[arg-type]
            return None
        return user

    async def increment_refresh_version(self, user_id: str) -> None:
        """Increment the refresh_token_version for a user to revoke existing refresh tokens."""
        # Load user and update version
        user = await self.get_user(user_id)
        if not user:
            return
        new_version = (user.refresh_token_version or 0) + 1
        await self.repository.update(user_id, {"refresh_token_version": new_version})
