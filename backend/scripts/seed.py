import asyncio
import json
import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import get_db
from app.domains.exercise.schemas.exercise_schemas import (
    ExerciseCreate,
    MovementCategory,
    ExerciseClassification,
    Equipment,
    TrainingAdaptation,
)
from app.domains.exercise.repositories.exercise_repository import (
    SQLAlchemyExerciseRepository,
)
# Import the related models to ensure SQLAlchemy can resolve all relationships
from app.domains.program.models.workout import WorkoutPhase
from app.domains.users.models.user import User


async def seed_exercises():
    """
    Seeds the database with an initial set of exercises.
    """
    print("Seeding exercise data...")
    db_session_generator = get_db()
    db = await anext(db_session_generator)
    try:
        exercise_repo = SQLAlchemyExerciseRepository(session=db)

        # Check if exercises already exist
        existing_exercises = await exercise_repo.search_exercises(filters={}, limit=1)
        if existing_exercises:
            print("Exercises already seeded. Skipping.")
            return

        with open("scripts/seed_data/exercises.json", "r") as f:
            exercises_to_create = json.load(f)

        for exercise_data in exercises_to_create:
            # Pydantic models expect enums, so we convert strings from JSON
            exercise_data["movement_category"] = MovementCategory(
                exercise_data["movement_category"]
            )
            exercise_data["exercise_classification"] = ExerciseClassification(
                exercise_data["exercise_classification"]
            )
            exercise_data["primary_equipment"] = Equipment(
                exercise_data["primary_equipment"]
            )
            exercise_data["primary_adaptations"] = [
                TrainingAdaptation(a) for a in exercise_data["primary_adaptations"]
            ]
            if exercise_data.get("secondary_adaptations"):
                exercise_data["secondary_adaptations"] = [
                    TrainingAdaptation(a)
                    for a in exercise_data["secondary_adaptations"]
                ]
            if exercise_data.get("alternative_equipment"):
                exercise_data["alternative_equipment"] = [
                    Equipment(e) for e in exercise_data["alternative_equipment"]
                ]

            exercise_create = ExerciseCreate(**exercise_data)
            await exercise_repo.create_exercise(exercise_create)
            print(f"Created exercise: {exercise_create.name}")

        print("Exercise data seeded successfully.")
    finally:
        # Gracefully close the database session
        try:
            await anext(db_session_generator)
        except StopAsyncIteration:
            pass


if __name__ == "__main__":
    asyncio.run(seed_exercises())