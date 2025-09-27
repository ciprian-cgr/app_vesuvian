from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domains.daily_state.models.contextual_recommendation import (
    RecommendationType,
    RecommendationPriority,
)


class ContextualRecommendationBase(BaseModel):
    type: RecommendationType
    priority: RecommendationPriority
    content: dict
    actions: dict
    expires_at: datetime


class ContextualRecommendationCreate(ContextualRecommendationBase):
    user_id: str


class ContextualRecommendation(ContextualRecommendationBase):
    id: str
    user_id: str
    user_response: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)