import pytest
from unittest.mock import AsyncMock
import uuid
from datetime import datetime

from app.domains.exercise.models.exercise_models import Exercise
from app.domains.exercise.schemas.exercise_schemas import (
    ExerciseCreate,
    MovementCategory,
    ExerciseClassification,
    Equipment,
    TrainingAdaptation,
    ExerciseResponse,
)
from app.domains.exercise.services.exercise_service import ExerciseService


def create_mock_exercise(**kwargs):
    """Creates a mock Exercise object with default values for validation."""
    defaults = {
        "id": str(uuid.uuid4()),
        "name": "Default Exercise",
        "aliases": [],
        "movement_category": MovementCategory.STRENGTH,
        "exercise_classification": ExerciseClassification.COMPOUND,
        "muscle_involvement": {},
        "primary_adaptations": [],
        "secondary_adaptations": [],
        "demands": {},
        "primary_equipment": Equipment.BODYWEIGHT,
        "alternative_equipment": [],
        "technique_complexity": 1,
        "contraindications": [],
        "prerequisites": [],
        "setup_instructions": "Default setup",
        "execution_cues": [],
        "common_mistakes": [],
        "safety_notes": [],
        "progressions": [],
        "regressions": [],
        "alternatives": [],
        "demonstration_url": None,
        "form_video_url": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    defaults.update(kwargs)
    return Exercise(**defaults)


class MockExerciseRepository:
    def __init__(self):
        self.create_exercise = AsyncMock()
        self.get_exercise_by_id = AsyncMock()
        self.search_exercises = AsyncMock()
        self.get_exercise_relationships = AsyncMock()
        self.update_exercise = AsyncMock()


@pytest.fixture
def mock_exercise_repo():
    return MockExerciseRepository()


@pytest.mark.asyncio
async def test_create_exercise_success(mock_exercise_repo):
    service = ExerciseService(exercise_repository=mock_exercise_repo)

    exercise_data = ExerciseCreate(
        name="Test Squat",
        aliases=["Back Squat"],
        movement_category=MovementCategory.STRENGTH,
        exercise_classification=ExerciseClassification.COMPOUND,
        muscle_involvement={"primary": ["quadriceps", "glutes"]},
        primary_adaptations=[TrainingAdaptation.MAXIMAL_STRENGTH],
        demands={"metabolic": 3, "cardiovascular": 2},
        primary_equipment=Equipment.BARBELL,
        technique_complexity=4,
        setup_instructions="Place the bar on your back.",
        execution_cues=["Keep your chest up.", "Break at the hips."],
    )

    created_exercise_id = str(uuid.uuid4())
    created_exercise = Exercise(
        id=created_exercise_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        **exercise_data.model_dump(),
    )

    mock_exercise_repo.create_exercise.return_value = created_exercise

    result = await service.create_exercise(exercise_data)

    assert isinstance(result, ExerciseResponse)
    assert str(result.id) == created_exercise_id
    assert result.name == "Test Squat"
    mock_exercise_repo.create_exercise.assert_awaited_once_with(exercise_data)


@pytest.mark.asyncio
async def test_search_exercises(mock_exercise_repo):
    service = ExerciseService(exercise_repository=mock_exercise_repo)

    exercise1_id = str(uuid.uuid4())
    exercise1 = create_mock_exercise(
        id=exercise1_id,
        name="Barbell Bench Press",
        movement_category=MovementCategory.STRENGTH,
        exercise_classification=ExerciseClassification.COMPOUND,
        primary_equipment=Equipment.BARBELL,
        primary_adaptations=[TrainingAdaptation.HYPERTROPHY],
        technique_complexity=3,
        setup_instructions="Lie on the bench.",
        execution_cues=["Lower bar to chest."],
    )

    mock_exercise_repo.search_exercises.return_value = [exercise1]

    filters = {"movement_category": MovementCategory.STRENGTH}
    results = await service.search_exercises(filters=filters, limit=10, offset=0)

    assert len(results) == 1
    assert str(results[0].id) == exercise1_id
    mock_exercise_repo.search_exercises.assert_awaited_once_with(
        filters=filters, limit=10, offset=0
    )


@pytest.mark.asyncio
async def test_get_exercise_with_relationships_found(mock_exercise_repo):
    service = ExerciseService(exercise_repository=mock_exercise_repo)

    exercise_id = str(uuid.uuid4())
    exercise = create_mock_exercise(
        id=exercise_id,
        name="Pull Up",
        movement_category=MovementCategory.STRENGTH,
        exercise_classification=ExerciseClassification.COMPOUND,
        primary_equipment=Equipment.PULL_UP_BAR,
        primary_adaptations=[TrainingAdaptation.MAXIMAL_STRENGTH],
        technique_complexity=3,
        setup_instructions="Grab the bar.",
        execution_cues=["Pull your chin over the bar."],
        progressions=[str(uuid.uuid4())],
    )

    mock_exercise_repo.get_exercise_by_id.return_value = exercise
    mock_exercise_repo.get_exercise_relationships.return_value = {
        "progressions": [], "regressions": [], "alternatives": []
    }

    result = await service.get_exercise_with_relationships(exercise_id=exercise_id)

    assert result is not None
    assert str(result["exercise"].id) == exercise_id
    assert "relationships" in result
    mock_exercise_repo.get_exercise_by_id.assert_awaited_once_with(exercise_id)
    mock_exercise_repo.get_exercise_relationships.assert_awaited_once_with(exercise_id)


@pytest.mark.asyncio
async def test_get_exercise_with_relationships_not_found(mock_exercise_repo):
    service = ExerciseService(exercise_repository=mock_exercise_repo)

    non_existent_id = str(uuid.uuid4())
    mock_exercise_repo.get_exercise_by_id.return_value = None

    result = await service.get_exercise_with_relationships(exercise_id=non_existent_id)

    assert result is None
    mock_exercise_repo.get_exercise_by_id.assert_awaited_once_with(non_existent_id)
    mock_exercise_repo.get_exercise_relationships.assert_not_called()