"""Users domain package re-exports models, schemas, repositories, services and router.

This package is a thin compatibility layer to help migrate to domain-oriented layout
without changing the existing implementations.
"""
# Re-export public domain symbols from the domain-local modules
from app.domains.users.models.user import User as UserModel
from app.domains.users.schemas.user import User, UserCreate, UserUpdate, Token
from app.domains.users.repositories.user import IUserRepository, UserRepository
from app.domains.users.services.user import UserService
from app.domains.users.routes.users import router as users_router
from app.domains.users.routes.auth import router as auth_router

__all__ = [
    "UserModel",
    "User",
    "UserCreate",
    "UserUpdate",
    "Token",
    "IUserRepository",
    "UserRepository",
    "UserService",
    "users_router",
    "auth_router",
]
