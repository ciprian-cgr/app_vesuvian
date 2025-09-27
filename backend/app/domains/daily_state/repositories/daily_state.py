from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.domains.daily_state.models import DailyState


class IDailyStateRepository(ABC):
    @abstractmethod
    async def get_by_user_and_date(
        self, user_id: str, date: date
    ) -> Optional[DailyState]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> DailyState:
        ...

    @abstractmethod
    async def update(
        self, user_id: str, date: date, obj_in: dict
    ) -> Optional[DailyState]:
        ...


class DailyStateRepository(BaseRepository[DailyState], IDailyStateRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(DailyState, db)

    async def get_by_user_and_date(
        self, user_id: str, date: date
    ) -> Optional[DailyState]:
        result = await self.db.execute(
            select(self.model).where(
                self.model.user_id == user_id, self.model.date == date
            )
        )
        return result.scalar_one_or_none()

    async def update(
        self, user_id: str, date: date, obj_in: Dict[str, Any]
    ) -> Optional[DailyState]:
        obj_in = {k: v for k, v in obj_in.items() if v is not None}
        if not obj_in:
            return await self.get_by_user_and_date(user_id, date)

        await self.db.execute(
            update(self.model)
            .where(self.model.user_id == user_id, self.model.date == date)
            .values(**obj_in)
        )
        await self.db.commit()
        return await self.get_by_user_and_date(user_id, date)