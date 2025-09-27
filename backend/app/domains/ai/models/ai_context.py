from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AIContext(Base):
    __tablename__ = "ai_contexts"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True, default=lambda: str(uuid4()))
    user_preferences = Column(JSON)
    patterns = Column(JSON)
    current_state = Column(JSON)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")