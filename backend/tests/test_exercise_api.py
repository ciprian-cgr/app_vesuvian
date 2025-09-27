import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

from app.domains.exercise.schemas.exercise_schemas import (
    MovementCategory,
    ExerciseClassification,
    Equipment,
    TrainingAdaptation,
)

pytestmark = pytest.mark.asyncio


async def test_create_exercise_api():
    """
    Test creating an exercise via the API by creating the client inside the test.
    """
    exercise_data = {
        "name": "API Test Squat",
        "aliases": ["API Back Squat"],
        "movement_category": MovementCategory.STRENGTH.value,
        "exercise_classification": ExerciseClassification.COMPOUND.value,
        "muscle_involvement": {"primary": ["quadriceps", "glutes"]},
        "primary_adaptations": [TrainingAdaptation.MAXIMAL_STRENGTH.value],
        "demands": {"metabolic": 3, "cardiovascular": 2},
        "primary_equipment": Equipment.BARBELL.value,
        "technique_complexity": 4,
        "setup_instructions": "Place the bar on your back.",
        "execution_cues": ["Keep your chest up.", "Break at the hips."],
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        response = await client.post("/api/v1/exercises/", json=exercise_data)

    assert response.status_code == 201, response.text
    created_exercise = response.json()
    assert created_exercise["name"] == "API Test Squat"
    assert "id" in created_exercise
    assert created_exercise["movement_category"] == "strength"