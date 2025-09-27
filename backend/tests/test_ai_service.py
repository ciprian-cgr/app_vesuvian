import pytest
from unittest.mock import AsyncMock

from app.domains.ai.models import AIContext
from app.domains.ai.services import AIService
from app.domains.ai.schemas import AIContextUpdate


class MockAIContextRepo:
    def __init__(self):
        self.get_by_user_id = AsyncMock()
        self.create = AsyncMock()
        self.update = AsyncMock()


@pytest.fixture
def mock_repo():
    return MockAIContextRepo()


@pytest.mark.asyncio
async def test_get_or_create_ai_context_exists(mock_repo):
    user_id = "user1"
    existing_context = AIContext(user_id=user_id, user_preferences={"theme": "dark"})
    mock_repo.get_by_user_id.return_value = existing_context

    service = AIService(mock_repo)
    result = await service.get_or_create_ai_context(user_id)

    assert result.user_id == user_id
    assert result.user_preferences["theme"] == "dark"
    mock_repo.get_by_user_id.assert_awaited_with(user_id)
    mock_repo.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_or_create_ai_context_creates_new(mock_repo):
    user_id = "user2"
    mock_repo.get_by_user_id.return_value = None

    created_context = AIContext(
        user_id=user_id, user_preferences={}, patterns={}, current_state={}
    )
    mock_repo.create.return_value = created_context

    service = AIService(mock_repo)
    result = await service.get_or_create_ai_context(user_id)

    assert result.user_id == user_id
    mock_repo.get_by_user_id.assert_awaited_with(user_id)
    mock_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_ai_context(mock_repo):
    user_id = "user1"
    update_data = AIContextUpdate(current_state={"mood": "energetic"})

    updated_context = AIContext(user_id=user_id, current_state={"mood": "energetic"})
    mock_repo.update.return_value = updated_context

    service = AIService(mock_repo)
    result = await service.update_ai_context(user_id, update_data)

    assert result.current_state["mood"] == "energetic"
    mock_repo.update.assert_awaited_once()