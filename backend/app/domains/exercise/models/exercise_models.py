import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    Enum as SAEnum,
    JSON,
    ForeignKey,
    Index,
    Table,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.domains.exercise.schemas.exercise_schemas import (
    MovementCategory,
    ExerciseClassification,
    Equipment,
)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, unique=True)
    aliases = Column(JSON)
    movement_category = Column(SAEnum(MovementCategory), nullable=False)
    exercise_classification = Column(SAEnum(ExerciseClassification), nullable=False)
    muscle_involvement = Column(JSON)
    primary_adaptations = Column(JSON)
    secondary_adaptations = Column(JSON)
    demands = Column(JSON)
    primary_equipment = Column(SAEnum(Equipment), nullable=False)
    alternative_equipment = Column(JSON)
    technique_complexity = Column(Integer, nullable=False)
    contraindications = Column(JSON)
    prerequisites = Column(JSON)
    setup_instructions = Column(Text)
    execution_cues = Column(JSON)
    common_mistakes = Column(JSON)
    safety_notes = Column(JSON)
    progressions = Column(JSON)
    regressions = Column(JSON)
    alternatives = Column(JSON)
    demonstration_url = Column(String)
    form_video_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        Index("ix_exercises_movement_category", "movement_category"),
        Index("ix_exercises_primary_equipment", "primary_equipment"),
        Index(
            "ix_exercises_movement_category_classification",
            "movement_category",
            "exercise_classification",
        ),
    )


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    phase_id = Column(String, ForeignKey("workout_phases.id"), nullable=False)
    exercise_id = Column(String, ForeignKey("exercises.id"), nullable=False)
    position = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(JSON, nullable=False)
    rest_seconds = Column(Integer, nullable=False)
    load = Column(JSON, nullable=False)
    tempo = Column(String)
    rpe_target = Column(Integer)
    superset_group = Column(String)
    coaching_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    exercise = relationship("Exercise")
    phase = relationship("WorkoutPhase", back_populates="workout_exercises")

    __table_args__ = (
        UniqueConstraint("phase_id", "position", name="uq_phase_position"),
        Index("ix_workout_exercises_phase_id", "phase_id"),
        Index("ix_workout_exercises_exercise_id", "exercise_id"),
    )


class UserExerciseData(Base):
    __tablename__ = "user_exercise_data"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    exercise_id = Column(String, ForeignKey("exercises.id"), primary_key=True)
    personal_records = Column(JSON)
    user_rating = Column(Integer)
    user_notes = Column(Text)
    form_mastery_level = Column(Integer, nullable=False)
    user_contraindications = Column(JSON)
    preferred_modifications = Column(JSON)
    total_sessions = Column(Integer, default=0, nullable=False)
    last_performed = Column(DateTime(timezone=True))
    progression_trend = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
    exercise = relationship("Exercise")