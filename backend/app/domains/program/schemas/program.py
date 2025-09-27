from datetime import datetime
from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict

from app.domains.program.models.program import ProgramType, CreatedBy, ProgramStatus


class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    program_type: ProgramType
    created_by: CreatedBy
    goal_analysis: Optional[dict] = None
    total_duration_weeks: int
    training_frequency: int
    session_duration_target: int


class ProgramCreate(ProgramBase):
    user_id: str


class ProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    current_week: Optional[int] = None
    user_satisfaction_score: Optional[float] = None
    status: Optional[ProgramStatus] = None


class Program(ProgramBase):
    id: str
    user_id: str
    current_week: int
    adaptation_history: Optional[List[Any]] = None
    ai_confidence_score: float
    user_satisfaction_score: Optional[float] = None
    status: ProgramStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)