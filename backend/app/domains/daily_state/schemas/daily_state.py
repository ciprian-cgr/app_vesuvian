from datetime import datetime, date
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict


class DailyStateBase(BaseModel):
    scheduled_session: Optional[dict] = None
    daily_priorities: Optional[dict] = None
    relevant_progress: Optional[dict] = None
    available_actions: Optional[dict] = None
    ai_recommendations: Optional[dict] = None


class DailyStateCreate(DailyStateBase):
    user_id: str
    date: date
    expires_at: datetime


class DailyStateUpdate(BaseModel):
    scheduled_session: Optional[dict] = None
    daily_priorities: Optional[dict] = None
    relevant_progress: Optional[dict] = None
    available_actions: Optional[dict] = None
    ai_recommendations: Optional[dict] = None
    expires_at: Optional[datetime] = None


class DailyState(DailyStateBase):
    user_id: str
    date: date
    generated_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)