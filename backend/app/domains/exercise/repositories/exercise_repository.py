from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import uuid

from sqlalchemy import and_, or_, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domains.exercise.models.exercise_models import Exercise
from app.domains.exercise.schemas.exercise_schemas import ExerciseCreate, ExerciseUpdate


class ExerciseRepositoryInterface(ABC):
    @abstractmethod
    async def create_exercise(self, exercise_data: ExerciseCreate) -> Exercise:
        """Creates a new exercise in the database."""
        pass

    @abstractmethod
    async def get_exercise_by_id(self, exercise_id: str) -> Optional[Exercise]:
        """Retrieves an exercise by its UUID."""
        pass

    @abstractmethod
    async def search_exercises(
        self, filters: Dict[str, Any], limit: int = 100, offset: int = 0
    ) -> List[Exercise]:
        """Searches and filters exercises from the database."""
        pass

    @abstractmethod
    async def get_exercise_relationships(
        self, exercise_id: str
    ) -> Dict[str, List[Exercise]]:
        """Retrieves related exercises (progressions, regressions, alternatives)."""
        pass

    @abstractmethod
    async def update_exercise(
        self, exercise_id: str, update_data: ExerciseUpdate
    ) -> Optional[Exercise]:
        """Updates an existing exercise in the database."""
        pass


class SQLAlchemyExerciseRepository(ExerciseRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_exercise(self, exercise_data: ExerciseCreate) -> Exercise:
        db_exercise = Exercise(**exercise_data.model_dump())
        self.session.add(db_exercise)
        await self.session.commit()
        await self.session.refresh(db_exercise)
        return db_exercise

    async def get_exercise_by_id(self, exercise_id: str) -> Optional[Exercise]:
        result = await self.session.execute(
            select(Exercise).filter(Exercise.id == exercise_id)
        )
        return result.scalars().first()

    async def search_exercises(
        self, filters: Dict[str, Any], limit: int = 100, offset: int = 0
    ) -> List[Exercise]:
        query = select(Exercise)

        for key, value in filters.items():
            if value is None:
                continue
            if key == "movement_category":
                query = query.filter(Exercise.movement_category == value)
            elif key == "exercise_classification":
                query = query.filter(Exercise.exercise_classification == value)
            elif key == "equipment":
                query = query.filter(
                    or_(
                        Exercise.primary_equipment == value,
                        Exercise.alternative_equipment.any(value),
                    )
                )
            elif key == "muscle_group":
                query = query.filter(
                    Exercise.muscle_involvement.cast(String).ilike(f"%{value}%")
                )
            elif key == "training_adaptation":
                query = query.filter(
                    Exercise.primary_adaptations.cast(String).ilike(f"%{value}%")
                )
            elif key == "search":
                search_term = f"%{value}%"
                query = query.filter(
                    or_(
                        Exercise.name.ilike(search_term),
                        Exercise.aliases.any(value),
                    )
                )

        query = query.order_by(Exercise.name).offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_exercise_relationships(
        self, exercise_id: str
    ) -> Dict[str, List[Exercise]]:
        exercise = await self.get_exercise_by_id(exercise_id)
        if not exercise:
            return {"progressions": [], "regressions": [], "alternatives": []}

        related_ids = (
            (exercise.progressions or [])
            + (exercise.regressions or [])
            + (exercise.alternatives or [])
        )
        if not related_ids:
            return {"progressions": [], "regressions": [], "alternatives": []}

        related_exercises_query = select(Exercise).filter(Exercise.id.in_(related_ids))
        result = await self.session.execute(related_exercises_query)
        related_exercises = {ex.id: ex for ex in result.scalars().all()}

        return {
            "progressions": [
                related_exercises[ex_id]
                for ex_id in (exercise.progressions or [])
                if ex_id in related_exercises
            ],
            "regressions": [
                related_exercises[ex_id]
                for ex_id in (exercise.regressions or [])
                if ex_id in related_exercises
            ],
            "alternatives": [
                related_exercises[ex_id]
                for ex_id in (exercise.alternatives or [])
                if ex_id in related_exercises
            ],
        }

    async def update_exercise(
        self, exercise_id: str, update_data: ExerciseUpdate
    ) -> Optional[Exercise]:
        exercise = await self.get_exercise_by_id(exercise_id)
        if not exercise:
            return None

        update_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(exercise, key, value)

        await self.session.commit()
        await self.session.refresh(exercise)
        return exercise