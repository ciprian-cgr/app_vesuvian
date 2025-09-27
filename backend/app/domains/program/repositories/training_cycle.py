from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.domains.program.models import TrainingCycle


class ITrainingCycleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[TrainingCycle]:
        ...

    @abstractmethod
    async def get_all_by_program_id(
        self, program_id: str, skip: int = 0, limit: int = 100
    ) -> List[TrainingCycle]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> TrainingCycle:
        ...


class TrainingCycleRepository(BaseRepository[TrainingCycle], ITrainingCycleRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(TrainingCycle, db)

    async def get_all_by_program_id(
        self, program_id: str, skip: int = 0, limit: int = 100
    ) -> List[TrainingCycle]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.program_id == program_id)
            .order_by(self.model.cycle_order)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()  # type: ignore[return-value]