"""
Authentication endpoints.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.core.config import get_settings
from app.core.security import create_access_token
from app.schemas.user import Token, UserCreate, User
from app.services.user import UserService

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=User)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user."""
    return await user_service.create_user(user_create)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """Login and get access token."""
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
