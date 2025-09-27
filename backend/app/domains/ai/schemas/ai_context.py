from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AIContextBase(BaseModel):
    user_preferences: Optional[dict] = None
    patterns: Optional[dict] = None
    current_state: Optional[dict] = None


class AIContextCreate(AIContextBase):
    user_id: str


class AIContextUpdate(BaseModel):
    user_preferences: Optional[dict] = None
    patterns: Optional[dict] = None
    current_state: Optional[dict] = None


class AIContext(AIContextBase):
    user_id: str
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)