import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AdaptationType(str, enum.Enum):
    AI_AUTOMATIC = "ai_automatic"
    USER_REQUESTED = "user_requested"
    WELLNESS_TRIGGERED = "wellness_triggered"
    PERFORMANCE_TRIGGERED = "performance_triggered"


class ProgramAdaptation(Base):
    __tablename__ = "program_adaptations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    program_id = Column(String, ForeignKey("programs.id"), nullable=False)
    adaptation_type = Column(SAEnum(AdaptationType), nullable=False)
    trigger_data = Column(JSON, nullable=False)
    changes_made = Column(JSON, nullable=False)
    effectiveness_tracking = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    program = relationship("Program", back_populates="adaptations")