"""
Base repository pattern implementation with common CRUD operations.
"""
from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from abc import ABC, abstractmethod

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.logging import LoggerMixin

ModelType = TypeVar("ModelType", bound=Base)


class IBaseRepository(ABC, Generic[ModelType]):
    """Interface for base repository operations."""
    
    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        pass
    
    @abstractmethod
    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create new entity."""
        pass
    
    @abstractmethod
    async def update(self, id: Any, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Update existing entity."""
        pass
    
    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete entity by ID."""
        pass


class BaseRepository(IBaseRepository[ModelType], LoggerMixin):
    """Base repository implementation with common CRUD operations."""
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    async def get_by_id(self, id: Any) -> Optional[ModelType]:
        """Get entity by ID."""
        try:
            result = await self.db.execute(
                select(self.model).where(self.model.id == id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            self.logger.error(f"Error getting {self.model.__name__} by id {id}: {e}")
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        try:
            result = await self.db.execute(
                select(self.model).offset(skip).limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            self.logger.error(f"Error getting all {self.model.__name__}: {e}")
            return []
    
    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        """Create new entity."""
        try:
            db_obj = self.model(**obj_in)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error creating {self.model.__name__}: {e}")
            raise
    
    async def update(self, id: Any, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """Update existing entity."""
        try:
            # Remove None values
            obj_in = {k: v for k, v in obj_in.items() if v is not None}
            
            if not obj_in:
                return await self.get_by_id(id)
            
            await self.db.execute(
                update(self.model).where(self.model.id == id).values(**obj_in)
            )
            await self.db.commit()
            return await self.get_by_id(id)
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error updating {self.model.__name__} {id}: {e}")
            raise
    
    async def delete(self, id: Any) -> bool:
        """Delete entity by ID."""
        try:
            result = await self.db.execute(
                delete(self.model).where(self.model.id == id)
            )
            await self.db.commit()
            return result.rowcount > 0
        except Exception as e:
            await self.db.rollback()
            self.logger.error(f"Error deleting {self.model.__name__} {id}: {e}")
            return False
