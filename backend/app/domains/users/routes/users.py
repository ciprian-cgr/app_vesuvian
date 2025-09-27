"""
User management endpoints.
"""
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_user_service
from app.core.security import verify_token
from app.domains.users.schemas.user import User, UserUpdate
from app.domains.users.services.user import UserService

router = APIRouter()


async def get_current_user(
    token_data: Dict[str, Any] = Depends(verify_token),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Get current authenticated user."""
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    user = await user_service.get_user(str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Convert ORM model to Pydantic schema
    return User.model_validate(user)


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
) -> User:
    """Get current user information."""
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Update current user information."""
    updated_user = await user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return User.model_validate(updated_user)


@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> List[User]:
    """Get all users (requires authentication)."""
    users = await user_service.get_users(skip=skip, limit=limit)
    return [User.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Get user by ID."""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return User.model_validate(user)
