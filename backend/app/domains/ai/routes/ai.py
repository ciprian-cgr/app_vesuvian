from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_ai_service
from app.domains.ai.schemas import AIContext, AIContextUpdate
from app.domains.ai.services import AIService
from app.domains.users.routes.users import get_current_user
from app.domains.users.schemas import User

router = APIRouter()


@router.get("/{user_id}/ai-context/", response_model=AIContext)
async def get_user_ai_context(
    user_id: str,
    ai_service: AIService = Depends(get_ai_service),
    current_user: User = Depends(get_current_user),
) -> AIContext:
    """
    Get the AI context for a specific user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access AI context for another user.",
        )
    context = await ai_service.get_or_create_ai_context(user_id)
    return context


@router.post("/{user_id}/ai-context/update/", response_model=AIContext)
async def update_user_ai_context(
    user_id: str,
    context_update: AIContextUpdate,
    ai_service: AIService = Depends(get_ai_service),
    current_user: User = Depends(get_current_user),
) -> AIContext:
    """
    Update the AI context for a specific user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update AI context for another user.",
        )

    updated_context = await ai_service.update_ai_context(
        user_id, context_update
    )
    if not updated_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="AI context not found"
        )
    return updated_context