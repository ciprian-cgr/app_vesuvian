from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.base_repository import BaseRepository
from app.domains.ai.models import AIContext


class IAIContextRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[AIContext]:
        ...

    @abstractmethod
    async def create(self, obj_in: dict) -> AIContext:
        ...

    @abstractmethod
    async def update(self, user_id: str, obj_in: dict) -> Optional[AIContext]:
        ...


class AIContextRepository(BaseRepository[AIContext], IAIContextRepository):
    def __init__(self, db: AsyncSession):
        # Pass AIContext model to BaseRepository
        super().__init__(AIContext, db)

    async def get_by_user_id(self, user_id: str) -> Optional[AIContext]:
        """Get AI context by user ID."""
        try:
            result = await self.db.execute(
                select(self.model).where(self.model.user_id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            self.logger.error(f"Error getting AIContext by user_id {user_id}: {e}")
            return None

    async def update(
        self, user_id: str, obj_in: Dict[str, Any]
    ) -> Optional[AIContext]:
        """Update AI context for a user."""
        try:
            obj_in = {k: v for k, v in obj_in.items() if v is not None}
            if not obj_in:
                return await self.get_by_user_id(user_id)

            await self.db.execute(
                update(self.model)
                .where(self.model.user_id == user_id)
                .values(**obj_in)
            )
            await self.db.commit()
            return await self.get_by_user_id(user_id)
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error updating AIContext for user_id {user_id}: {e}")
            raise

    # Override get_by_id to use the correct primary key column
    async def get_by_id(self, id: str) -> Optional[AIContext]:
        return await self.get_by_user_id(id)