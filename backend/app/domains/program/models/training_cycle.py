import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CycleFocus(str, enum.Enum):
    ANATOMICAL_ADAPTATION = "anatomical_adaptation"
    STRENGTH_BUILDING = "strength_building"
    HYPERTROPHY_EMPHASIS = "hypertrophy_emphasis"
    STRENGTH_PEAKING = "strength_peaking"


class VolumeEmphasis(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class IntensityProgression(str, enum.Enum):
    LINEAR = "linear"
    UNDULATING = "undulating"
    AUTO_REGULATED = "auto_regulated"


class TrainingCycle(Base):
    __tablename__ = "training_cycles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    name = Column(String, nullable=False)
    cycle_order = Column(Integer, nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    cycle_focus = Column(SAEnum(CycleFocus), nullable=False)
    volume_emphasis = Column(SAEnum(VolumeEmphasis), nullable=False)
    intensity_progression = Column(SAEnum(IntensityProgression), nullable=False)
    adaptation_triggers = Column(JSON)
    success_criteria = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    program = relationship("Program", back_populates="cycles")
    workouts = relationship("Workout", back_populates="cycle", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("program_id", "cycle_order", name="uq_program_cycle_order"),
    )