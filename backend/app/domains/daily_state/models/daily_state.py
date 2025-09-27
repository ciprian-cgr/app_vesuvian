import enum
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Date,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class DailyState(Base):
    __tablename__ = "daily_states"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    date = Column(Date, primary_key=True)

    scheduled_session = Column(JSON)
    daily_priorities = Column(JSON)
    relevant_progress = Column(JSON)
    available_actions = Column(JSON)
    ai_recommendations = Column(JSON)

    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_user_date"),
        Index("ix_daily_states_user_id_expires_at", "user_id", "expires_at"),
    )