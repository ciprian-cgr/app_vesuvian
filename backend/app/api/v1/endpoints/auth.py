"""
Authentication endpoints.
"""
from datetime import timedelta

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.domains.users.schemas.user import Token, UserCreate, User
from app.domains.users.services.user import UserService
from app.core.security import set_refresh_cookie, delete_refresh_cookie, REFRESH_COOKIE_NAME

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=User)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> User:
    """Register a new user."""
    created = await user_service.create_user(user_create)
    # Convert ORM instance to Pydantic schema for response_model compatibility
    return User.model_validate(created)


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> Token:
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
    # include refresh token version in payload
    refresh_token = create_refresh_token(data={"sub": str(user.id), "ver": user.refresh_token_version})

    # set HttpOnly cookie for refresh token on response
    set_refresh_cookie(response, refresh_token)
    return Token(access_token=access_token, token_type="bearer")




@router.post("/refresh", response_model=Token)
async def refresh_token(request: Request, response: Response, user_service: UserService = Depends(get_user_service)) -> Token:
    """Refresh access token using refresh token from HttpOnly cookie."""
    refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing refresh token cookie")

    token_data = verify_refresh_token(refresh)
    user_id = token_data.get("sub")
    token_ver: Any = token_data.get("ver")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    # validate stored token version for revocation
    user = await user_service.get_user(str(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    try:
        token_ver_int = int(token_ver) if token_ver is not None else None
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if token_ver_int != int(user.refresh_token_version):
        # token is revoked
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user_id)}, expires_delta=access_token_expires)
    # rotate refresh token and keep same version
    refresh_token = create_refresh_token(data={"sub": str(user_id), "ver": user.refresh_token_version})

    # set rotated refresh token on response cookie
    set_refresh_cookie(response, refresh_token)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/logout")
async def logout(response: Response, request: Request, user_service: UserService = Depends(get_user_service)) -> Dict[str, str]:
    """Logout: revoke refresh tokens by bumping user's refresh_token_version and clearing cookie."""
    # If user is identified via cookie, attempt to revoke their tokens
    refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    if refresh:
        try:
            token_data = verify_refresh_token(refresh)
            user_id = token_data.get("sub")
            if user_id:
                # increment stored version to revoke existing refresh tokens
                await user_service.increment_refresh_version(str(user_id))
        except Exception:
            # ignore errors during logout
            pass

    delete_refresh_cookie(response)
    return {"detail": "logged out"}
