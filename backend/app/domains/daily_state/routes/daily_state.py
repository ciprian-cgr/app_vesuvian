from datetime import date, datetime
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query, HTTPException, status

from app.api.dependencies import get_daily_state_service
from app.domains.daily_state.schemas import DailyState, ContextualRecommendation
from app.domains.daily_state.services import DailyStateService
from app.domains.users.routes.users import get_current_user
from app.domains.users.schemas import User

router = APIRouter()


@router.get("/{user_id}/daily-state/", response_model=DailyState)
async def get_daily_state_for_user(
    user_id: str,
    date_param: date = Query(None, alias="date"),
    service: DailyStateService = Depends(get_daily_state_service),
    current_user: User = Depends(get_current_user),
) -> DailyState:
    """
    Get the simplified daily view for a user.
    Defaults to today if no date is provided.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access daily state for another user.",
        )
    target_date = date_param if date_param else datetime.utcnow().date()
    return await service.get_daily_state(user_id, target_date)


@router.post("/{user_id}/daily-action/", response_model=Dict[str, Any])
async def execute_daily_action(
    user_id: str,
    action_data: Dict[str, Any],
    service: DailyStateService = Depends(get_daily_state_service),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Execute a quick action from the daily view.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot perform actions for another user.",
        )
    return await service.process_daily_action(user_id, action_data)


@router.get(
    "/{user_id}/contextual-recommendations/",
    response_model=List[ContextualRecommendation],
)
async def get_contextual_recommendations_for_user(
    user_id: str,
    service: DailyStateService = Depends(get_daily_state_service),
    current_user: User = Depends(get_current_user),
) -> List[ContextualRecommendation]:
    """
    Get active contextual recommendations for a user.
    """
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access recommendations for another user.",
        )
    return await service.get_active_recommendations(user_id)

# Note: The context-update endpoint from ticket 1.1.2 is functionally identical
# to the one created for the AI domain. We will use that one to avoid duplication.