import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    JSON,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class RecommendationType(str, enum.Enum):
    SESSION_MODIFICATION = "session_modification"
    WELLNESS_ACTION = "wellness_action"
    MOTIVATIONAL = "motivational"
    EDUCATIONAL = "educational"


class RecommendationPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ContextualRecommendation(Base):
    __tablename__ = "contextual_recommendations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    type = Column(SAEnum(RecommendationType), nullable=False)
    priority = Column(SAEnum(RecommendationPriority), nullable=False)

    content = Column(JSON, nullable=False)
    actions = Column(JSON, nullable=False)
    user_response = Column(JSON, nullable=True)

    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

    __table_args__ = (
        Index("ix_recommendations_user_id_expires_at", "user_id", "expires_at"),
        Index("ix_recommendations_priority_created_at", "priority", "created_at"),
    )