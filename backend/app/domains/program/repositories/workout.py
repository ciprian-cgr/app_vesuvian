from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.domains.program.models import Workout


class IWorkoutRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Workout]:
        ...

    @abstractmethod
    async def get_all_by_cycle_id(
        self, cycle_id: str, skip: int = 0, limit: int = 100
    ) -> List[Workout]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> Workout:
        ...


class WorkoutRepository(BaseRepository[Workout], IWorkoutRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Workout, db)

    async def get_all_by_cycle_id(
        self, cycle_id: str, skip: int = 0, limit: int = 100
    ) -> List[Workout]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.cycle_id == cycle_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()  # type: ignore[return-value]