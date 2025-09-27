from typing import List, Optional, Dict, Any

from app.domains.exercise.repositories.exercise_repository import (
    ExerciseRepositoryInterface,
)
from app.domains.exercise.schemas.exercise_schemas import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
    Equipment,
)


class ExerciseService:
    def __init__(self, exercise_repository: ExerciseRepositoryInterface):
        self.exercise_repository = exercise_repository

    async def create_exercise(self, exercise_data: ExerciseCreate) -> ExerciseResponse:
        exercise = await self.exercise_repository.create_exercise(exercise_data)
        return ExerciseResponse.model_validate(exercise)

    async def search_exercises(
        self, filters: Dict[str, Any], limit: int, offset: int
    ) -> List[ExerciseResponse]:
        exercises = await self.exercise_repository.search_exercises(
            filters=filters, limit=limit, offset=offset
        )
        return [ExerciseResponse.model_validate(ex) for ex in exercises]

    async def get_exercise_with_relationships(
        self, exercise_id: str, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        exercise = await self.exercise_repository.get_exercise_by_id(exercise_id)
        if not exercise:
            return None

        relationships = await self.exercise_repository.get_exercise_relationships(
            exercise_id
        )

        return {
            "exercise": ExerciseResponse.model_validate(exercise),
            "relationships": {
                "progressions": [
                    ExerciseResponse.model_validate(p) for p in relationships["progressions"]
                ],
                "regressions": [
                    ExerciseResponse.model_validate(r) for r in relationships["regressions"]
                ],
                "alternatives": [
                    ExerciseResponse.model_validate(a) for a in relationships["alternatives"]
                ],
            },
        }

    async def find_exercise_substitutions(
        self,
        exercise_id: str,
        reason: Optional[str] = None,
        available_equipment: Optional[List[Equipment]] = None,
    ) -> Dict[str, List[ExerciseResponse]]:
        exercise = await self.exercise_repository.get_exercise_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        # This is a simplified implementation. A real-world scenario would involve
        # more complex logic based on the reason and available equipment.
        relationships = await self.exercise_repository.get_exercise_relationships(
            exercise_id
        )

        substitutions = {
            "progressions": [
                ExerciseResponse.model_validate(p) for p in relationships["progressions"]
            ],
            "regressions": [
                ExerciseResponse.model_validate(r) for r in relationships["regressions"]
            ],
            "alternatives": [
                ExerciseResponse.model_validate(a) for a in relationships["alternatives"]
            ],
        }
        return substitutions

    async def update_exercise(
        self, exercise_id: str, update_data: ExerciseUpdate
    ) -> Optional[ExerciseResponse]:
        exercise = await self.exercise_repository.update_exercise(
            exercise_id, update_data
        )
        if not exercise:
            return None
        return ExerciseResponse.model_validate(exercise)