"""
API dependencies for dependency injection.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.ai.repositories import AIContextRepository
from app.domains.ai.services import AIService
from app.domains.program.repositories import (
    ProgramRepository,
    TrainingCycleRepository,
    WorkoutRepository,
)
from app.domains.program.services import ProgramService
from app.domains.users import UserRepository, UserService


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    """Get user service instance wired with repository implementation."""
    repository = UserRepository(db)
    return UserService(repository)


def get_program_service(db: AsyncSession = Depends(get_db)) -> ProgramService:
    """Get program service instance wired with repository implementations."""
    return ProgramService(
        program_repo=ProgramRepository(db),
        cycle_repo=TrainingCycleRepository(db),
        workout_repo=WorkoutRepository(db),
    )


from app.domains.daily_state.repositories import (
    ContextualRecommendationRepository,
    DailyStateRepository,
)
from app.domains.daily_state.services import DailyStateService


def get_ai_service(db: AsyncSession = Depends(get_db)) -> AIService:
    """Get AI service instance wired with repository implementation."""
    repository = AIContextRepository(db)
    return AIService(repository)


def get_daily_state_service(db: AsyncSession = Depends(get_db)) -> DailyStateService:
    """Get daily state service instance wired with repository implementations."""
    return DailyStateService(
        daily_state_repo=DailyStateRepository(db),
        recommendation_repo=ContextualRecommendationRepository(db),
    )
