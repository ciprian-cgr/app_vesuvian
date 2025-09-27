from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict

from app.domains.program.models.training_cycle import (
    CycleFocus,
    VolumeEmphasis,
    IntensityProgression,
)


class TrainingCycleBase(BaseModel):
    name: str
    cycle_order: int
    duration_weeks: int
    cycle_focus: CycleFocus
    volume_emphasis: VolumeEmphasis
    intensity_progression: IntensityProgression
    adaptation_triggers: Optional[list] = None
    success_criteria: Optional[dict] = None


class TrainingCycleCreate(TrainingCycleBase):
    program_id: str


class TrainingCycle(TrainingCycleBase):
    id: str
    program_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)