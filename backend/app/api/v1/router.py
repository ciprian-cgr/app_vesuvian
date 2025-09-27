"""
Main API router for version 1.
"""
from fastapi import APIRouter

from app.domains.users.routes.auth import router as auth_router
from app.domains.users.routes.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
