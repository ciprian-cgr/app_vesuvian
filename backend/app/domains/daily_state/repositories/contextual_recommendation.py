from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.domains.daily_state.models import ContextualRecommendation


class IContextualRecommendationRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ContextualRecommendation]:
        ...

    @abstractmethod
    async def get_active_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[ContextualRecommendation]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> ContextualRecommendation:
        ...


class ContextualRecommendationRepository(
    BaseRepository[ContextualRecommendation], IContextualRecommendationRepository
):
    def __init__(self, db: AsyncSession):
        super().__init__(ContextualRecommendation, db)

    async def get_active_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[ContextualRecommendation]:
        now = datetime.utcnow()
        result = await self.db.execute(
            select(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.expires_at > now,
            )
            .order_by(self.model.priority, self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()  # type: ignore[return-value]