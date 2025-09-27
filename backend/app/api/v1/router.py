"""
Main API router for version 1.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import ai, daily_state, programs
from app.domains.users.routes.auth import router as auth_router
from app.domains.users.routes.users import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(programs.router, prefix="/programs", tags=["programs"])
api_router.include_router(ai.router, prefix="/users", tags=["ai"])
api_router.include_router(daily_state.router, prefix="/users", tags=["daily-state"])