"""Users domain package re-exports models, schemas, repositories, services and router.

This package is a thin compatibility layer to help migrate to domain-oriented layout
without changing the existing implementations.
"""
# Re-export public domain symbols from the domain-local modules
from app.domains.users.models.user import User as UserModel
from app.domains.users.schemas.user import User, UserCreate, UserUpdate, Token
from app.domains.users.repositories.user import IUserRepository, UserRepository
from app.domains.users.services.user import UserService

__all__ = [
    "UserModel",
    "User",
    "UserCreate",
    "UserUpdate",
    "Token",
    "IUserRepository",
    "UserRepository",
    "UserService",
]
