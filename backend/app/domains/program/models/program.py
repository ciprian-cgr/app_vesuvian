import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Float,
    DateTime,
    Enum as SAEnum,
    JSON,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ProgramType(str, enum.Enum):
    AI_GENERATED = "ai_generated"
    USER_CREATED = "user_created"
    TEMPLATE = "template"
    HYBRID = "hybrid"


class CreatedBy(str, enum.Enum):
    AI = "ai"
    USER = "user"
    TEMPLATE = "template"


class ProgramStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Program(Base):
    __tablename__ = "programs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    program_type = Column(SAEnum(ProgramType), nullable=False)
    created_by = Column(SAEnum(CreatedBy), nullable=False)
    goal_analysis = Column(JSON)
    total_duration_weeks = Column(Integer, nullable=False)
    current_week = Column(Integer, default=1, nullable=False)
    training_frequency = Column(Integer, nullable=False)
    session_duration_target = Column(Integer, nullable=False)
    adaptation_history = Column(JSON)
    ai_confidence_score = Column(Float, default=0.0)
    user_satisfaction_score = Column(Float, nullable=True)
    status = Column(SAEnum(ProgramStatus), default=ProgramStatus.DRAFT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
    cycles = relationship("TrainingCycle", back_populates="program", cascade="all, delete-orphan")
    adaptations = relationship("ProgramAdaptation", back_populates="program", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_programs_user_id_status", "user_id", "status"),
        Index("ix_programs_created_at", "created_at"),
    )