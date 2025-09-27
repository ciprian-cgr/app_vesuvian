from abc import ABC, abstractmethod
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseRepository
from app.domains.program.models import Program
from app.domains.program.models.program import ProgramStatus


class IProgramRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Program]:
        ...

    @abstractmethod
    async def get_all_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Program]:
        ...

    @abstractmethod
    async def get_by_user_and_status(
        self, user_id: str, status: ProgramStatus, skip: int = 0, limit: int = 100
    ) -> List[Program]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> Program:
        ...

    @abstractmethod
    async def update(self, id: str, obj_in: dict) -> Optional[Program]:
        ...


class ProgramRepository(BaseRepository[Program], IProgramRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Program, db)

    async def get_all_by_user_id(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[Program]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()  # type: ignore[return-value]

    async def get_by_user_and_status(
        self, user_id: str, status: ProgramStatus, skip: int = 0, limit: int = 100
    ) -> List[Program]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.user_id == user_id, self.model.status == status)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()  # type: ignore[return-value]