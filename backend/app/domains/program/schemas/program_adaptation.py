from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domains.program.models.program_adaptation import AdaptationType


class ProgramAdaptationBase(BaseModel):
    adaptation_type: AdaptationType
    trigger_data: dict
    changes_made: dict
    effectiveness_tracking: Optional[dict] = None


class ProgramAdaptationCreate(ProgramAdaptationBase):
    program_id: str


class ProgramAdaptation(ProgramAdaptationBase):
    id: str
    program_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)