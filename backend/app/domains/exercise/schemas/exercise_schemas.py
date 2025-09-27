from enum import Enum

class Equipment(str, Enum):
    BODYWEIGHT = "bodyweight"
    FREE_WEIGHTS = "free_weights"
    MINIMAL_EQUIPMENT = "minimal_equipment"
    FULL_GYM = "full_gym"
    BARBELL = "barbell"
    DUMBBELLS = "dumbbells"
    KETTLEBELLS = "kettlebells"
    RESISTANCE_BANDS = "resistance_bands"
    PULL_UP_BAR = "pull_up_bar"
    SUSPENSION_TRAINER = "suspension_trainer"
    MEDICINE_BALL = "medicine_ball"
    CABLE_MACHINE = "cable_machine"
    MACHINES = "machines"

class MovementCategory(str, Enum):
    STRENGTH = "strength"
    POWER = "power"
    ENDURANCE = "endurance"
    MOBILITY = "mobility"
    BALANCE = "balance"
    COORDINATION = "coordination"

class ExerciseClassification(str, Enum):
    COMPOUND = "compound"
    ISOLATION = "isolation"
    ACCESSORY = "accessory"
    OLYMPIC = "olympic"
    PLYOMETRIC = "plyometric"

class TrainingAdaptation(str, Enum):
    MAXIMAL_STRENGTH = "maximal_strength"
    HYPERTROPHY = "hypertrophy"
    MUSCULAR_ENDURANCE = "muscular_endurance"
    POWER = "power"
    STRENGTH_ENDURANCE = "strength_endurance"
    ANAEROBIC_CAPACITY = "anaerobic_capacity"
    AEROBIC_CAPACITY = "aerobic_capacity"

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    aliases: List[str] = Field(default_factory=list)
    movement_category: MovementCategory
    exercise_classification: ExerciseClassification
    muscle_involvement: Dict[str, Any] = Field(default_factory=dict)
    primary_adaptations: List[TrainingAdaptation]
    secondary_adaptations: List[TrainingAdaptation] = Field(default_factory=list)
    demands: Dict[str, Any] = Field(default_factory=dict)
    primary_equipment: Equipment
    alternative_equipment: List[Equipment] = Field(default_factory=list)
    technique_complexity: int = Field(..., ge=1, le=5)
    contraindications: List[str] = Field(default_factory=list)
    prerequisites: List[str] = Field(default_factory=list)
    setup_instructions: str
    execution_cues: List[str]
    common_mistakes: List[str] = Field(default_factory=list)
    safety_notes: List[str] = Field(default_factory=list)
    progressions: List[str] = Field(default_factory=list)
    regressions: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)
    demonstration_url: Optional[str] = None
    form_video_url: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    aliases: Optional[List[str]] = None
    movement_category: Optional[MovementCategory] = None
    exercise_classification: Optional[ExerciseClassification] = None
    muscle_involvement: Optional[Dict[str, Any]] = None
    primary_adaptations: Optional[List[TrainingAdaptation]] = None
    secondary_adaptations: Optional[List[TrainingAdaptation]] = None
    demands: Optional[Dict[str, Any]] = None
    primary_equipment: Optional[Equipment] = None
    alternative_equipment: Optional[List[Equipment]] = None
    technique_complexity: Optional[int] = Field(None, ge=1, le=5)
    contraindications: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    setup_instructions: Optional[str] = None
    execution_cues: Optional[List[str]] = None
    common_mistakes: Optional[List[str]] = None
    safety_notes: Optional[List[str]] = None
    progressions: Optional[List[str]] = None
    regressions: Optional[List[str]] = None
    alternatives: Optional[List[str]] = None
    demonstration_url: Optional[str] = None
    form_video_url: Optional[str] = None

class ExerciseResponse(ExerciseBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExerciseRelationshipResponse(BaseModel):
    progressions: List[ExerciseResponse]
    regressions: List[ExerciseResponse]
    alternatives: List[ExerciseResponse]


class ExerciseDetailResponse(BaseModel):
    exercise: ExerciseResponse
    relationships: ExerciseRelationshipResponse


class WorkoutExerciseBase(BaseModel):
    phase_id: uuid.UUID
    exercise_id: uuid.UUID
    position: int = Field(..., ge=0)
    sets: int = Field(..., gt=0)
    reps: Dict[str, Any]
    rest_seconds: int = Field(..., ge=0)
    load: Dict[str, Any]
    tempo: Optional[str] = None
    rpe_target: Optional[int] = Field(None, ge=1, le=10)
    superset_group: Optional[str] = None
    coaching_notes: Optional[str] = None


class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass


class WorkoutExerciseUpdate(BaseModel):
    position: Optional[int] = Field(None, ge=0)
    sets: Optional[int] = Field(None, gt=0)
    reps: Optional[Dict[str, Any]] = None
    rest_seconds: Optional[int] = Field(None, ge=0)
    load: Optional[Dict[str, Any]] = None
    tempo: Optional[str] = None
    rpe_target: Optional[int] = Field(None, ge=1, le=10)
    superset_group: Optional[str] = None
    coaching_notes: Optional[str] = None


class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserExerciseDataBase(BaseModel):
    user_id: uuid.UUID
    exercise_id: uuid.UUID
    personal_records: Dict[str, Any] = Field(default_factory=dict)
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    user_notes: Optional[str] = None
    form_mastery_level: int = Field(..., ge=1, le=5)
    user_contraindications: List[str] = Field(default_factory=list)
    preferred_modifications: List[str] = Field(default_factory=list)
    total_sessions: int = Field(default=0, ge=0)
    last_performed: Optional[datetime] = None
    progression_trend: str


class UserExerciseDataCreate(UserExerciseDataBase):
    pass


class UserExerciseDataUpdate(BaseModel):
    personal_records: Optional[Dict[str, Any]] = None
    user_rating: Optional[int] = Field(None, ge=1, le=5)
    user_notes: Optional[str] = None
    form_mastery_level: Optional[int] = Field(None, ge=1, le=5)
    user_contraindications: Optional[List[str]] = None
    preferred_modifications: Optional[List[str]] = None
    total_sessions: Optional[int] = Field(None, ge=0)
    last_performed: Optional[datetime] = None
    progression_trend: Optional[str] = None


class UserExerciseDataResponse(UserExerciseDataBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True