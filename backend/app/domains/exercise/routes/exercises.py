from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_exercise_service
from app.domains.exercise.schemas.exercise_schemas import (
    ExerciseResponse,
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseDetailResponse,
    MovementCategory,
    ExerciseClassification,
    Equipment,
    TrainingAdaptation,
)
from app.domains.exercise.services.exercise_service import ExerciseService
from app.domains.users.routes.users import get_current_user

# A placeholder for a dependency that would get the current user's ID.
# In a real application, this would come from your authentication system.
async def get_current_user_id() -> Optional[str]:
    # For now, we'll return None as the user system isn't fully integrated.
    return None


router = APIRouter()


@router.post(
    "/",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
async def create_exercise(
    exercise_data: ExerciseCreate,
    exercise_service: ExerciseService = Depends(get_exercise_service),
) -> ExerciseResponse:
    """Create a new exercise in the library."""
    try:
        exercise = await exercise_service.create_exercise(exercise_data)
        return exercise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/", response_model=List[ExerciseResponse])
async def search_exercises(
    movement_category: Optional[MovementCategory] = Query(None),
    exercise_classification: Optional[ExerciseClassification] = Query(None),
    equipment: Optional[Equipment] = Query(None),
    muscle_group: Optional[str] = Query(None),
    training_adaptation: Optional[TrainingAdaptation] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    exercise_service: ExerciseService = Depends(get_exercise_service),
) -> List[ExerciseResponse]:
    """Search and filter exercise library with comprehensive filtering options."""
    filters = {
        "movement_category": movement_category,
        "exercise_classification": exercise_classification,
        "equipment": equipment,
        "muscle_group": muscle_group,
        "training_adaptation": training_adaptation,
        "search": search,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    try:
        exercises = await exercise_service.search_exercises(
            filters=filters, limit=limit, offset=offset
        )
        return exercises
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{exercise_id}", response_model=ExerciseDetailResponse)
async def get_exercise_detail(
    exercise_id: str,
    exercise_service: ExerciseService = Depends(get_exercise_service),
    user_id: Optional[str] = Depends(get_current_user_id),
) -> ExerciseDetailResponse:
    """Get detailed exercise information with related exercises."""
    try:
        exercise_detail_data = await exercise_service.get_exercise_with_relationships(
            exercise_id=exercise_id, user_id=user_id
        )
        if not exercise_detail_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
            )
        return ExerciseDetailResponse.model_validate(exercise_detail_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{exercise_id}/substitutions", response_model=Dict[str, List[ExerciseResponse]])
async def get_exercise_substitutions(
    exercise_id: str,
    reason: Optional[str] = Query(None, description="Reason for substitution"),
    available_equipment: Optional[List[Equipment]] = Query(None),
    exercise_service: ExerciseService = Depends(get_exercise_service),
) -> Dict[str, List[ExerciseResponse]]:
    """Find exercise alternatives based on various criteria."""
    try:
        substitutions = await exercise_service.find_exercise_substitutions(
            exercise_id=exercise_id,
            reason=reason,
            available_equipment=available_equipment,
        )
        return substitutions
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: str,
    exercise_data: ExerciseUpdate,
    exercise_service: ExerciseService = Depends(get_exercise_service),
    # current_user: User = Depends(get_current_active_user), # Add auth later
) -> ExerciseResponse:
    """Update an exercise in the library."""
    updated_exercise = await exercise_service.update_exercise(
        exercise_id, exercise_data
    )
    if not updated_exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found"
        )
    return updated_exercise