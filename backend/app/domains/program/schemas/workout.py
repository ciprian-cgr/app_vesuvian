from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domains.program.models.workout import (
    WorkoutType,
    TrainingStyle,
    EquipmentRequired,
    AdaptationFlexibility,
)


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    workout_type: WorkoutType
    training_style: TrainingStyle
    estimated_duration: dict
    equipment_required: EquipmentRequired
    adaptation_flexibility: AdaptationFlexibility
    auto_progression_enabled: bool = True


class WorkoutCreate(WorkoutBase):
    cycle_id: str


class Workout(WorkoutBase):
    id: str
    cycle_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)