import pytest
from unittest.mock import AsyncMock

from app.domains.program.models import Program
from app.domains.program.schemas import ProgramCreate
from app.domains.program.services import ProgramService


class MockProgramRepo:
    def __init__(self):
        self.create = AsyncMock()
        self.get_by_id = AsyncMock()
        self.update = AsyncMock()


class MockCycleRepo:
    def __init__(self):
        self.get_all_by_program_id = AsyncMock()


class MockWorkoutRepo:
    def __init__(self):
        self.get_all_by_cycle_id = AsyncMock()


@pytest.fixture
def mock_repos():
    return MockProgramRepo(), MockCycleRepo(), MockWorkoutRepo()


@pytest.mark.asyncio
async def test_create_program_success(mock_repos):
    program_repo, cycle_repo, workout_repo = mock_repos

    program_create = ProgramCreate(
        user_id="user1",
        name="Test Program",
        description="A test program.",
        program_type="user_created",
        created_by="user",
        total_duration_weeks=4,
        training_frequency=3,
        session_duration_target=60,
    )

    created_program = Program(**program_create.model_dump(), id="prog1")
    program_repo.create.return_value = created_program
    program_repo.update.return_value = created_program

    service = ProgramService(program_repo, cycle_repo, workout_repo)

    result = await service.create_program(program_create)

    assert result.id == "prog1"
    assert result.name == "Test Program"
    program_repo.create.assert_awaited_once()
    program_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_full_program_details_not_found(mock_repos):
    program_repo, cycle_repo, workout_repo = mock_repos
    program_repo.get_by_id.return_value = None

    service = ProgramService(program_repo, cycle_repo, workout_repo)

    result = await service.get_full_program_details("nonexistent_id")

    assert result is None
    program_repo.get_by_id.assert_awaited_with("nonexistent_id")