import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Boolean,
    JSON,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class WorkoutPhaseType(str, enum.Enum):
    WARMUP = "warmup"
    MAIN = "main"
    ACCESSORY = "accessory"
    COOLDOWN = "cooldown"


class WorkoutType(str, enum.Enum):
    STRENGTH_FOCUSED = "strength_focused"
    HYPERTROPHY_FOCUSED = "hypertrophy_focused"
    CARDIO_INTERVALS = "cardio_intervals"
    MOBILITY_FOCUSED = "mobility_focused"


class TrainingStyle(str, enum.Enum):
    TRADITIONAL_SETS = "traditional_sets"
    SUPERSET = "superset"
    CIRCUIT = "circuit"
    REST_PAUSE = "rest_pause"


class EquipmentRequired(str, enum.Enum):
    BODYWEIGHT = "bodyweight"
    FREE_WEIGHTS = "free_weights"
    MINIMAL_EQUIPMENT = "minimal_equipment"
    FULL_GYM = "full_gym"


class AdaptationFlexibility(str, enum.Enum):
    RIGID = "rigid"
    MODERATE = "moderate"
    HIGH = "high"


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    cycle_id = Column(String, ForeignKey("training_cycles.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    workout_type = Column(SAEnum(WorkoutType), nullable=False)
    training_style = Column(SAEnum(TrainingStyle), nullable=False)
    estimated_duration = Column(JSON, nullable=False)
    equipment_required = Column(SAEnum(EquipmentRequired), nullable=False)
    adaptation_flexibility = Column(SAEnum(AdaptationFlexibility), nullable=False)
    auto_progression_enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    cycle = relationship("TrainingCycle", back_populates="workouts")
    phases = relationship("WorkoutPhase", back_populates="workout", cascade="all, delete-orphan")


class WorkoutPhase(Base):
    __tablename__ = "workout_phases"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    workout_id = Column(String, ForeignKey("workouts.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    phase_type = Column(SAEnum(WorkoutPhaseType), nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    workout = relationship("Workout", back_populates="phases")
    workout_exercises = relationship("WorkoutExercise", back_populates="phase", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("workout_id", "position", name="uq_workout_phase_position"),
    )