import pytest
from unittest.mock import AsyncMock
from datetime import date, datetime, timedelta

from app.domains.daily_state.models import DailyState
from app.domains.daily_state.services import DailyStateService


class MockDailyStateRepo:
    def __init__(self):
        self.get_by_user_and_date = AsyncMock()
        self.create = AsyncMock()
        self.update = AsyncMock()


class MockRecommendationRepo:
    def __init__(self):
        self.get_active_by_user_id = AsyncMock()


@pytest.fixture
def mock_repos():
    return MockDailyStateRepo(), MockRecommendationRepo()


@pytest.mark.asyncio
async def test_get_daily_state_returns_cached_if_valid(mock_repos):
    daily_state_repo, recommendation_repo = mock_repos
    user_id = "user1"
    today = datetime.utcnow().date()

    cached_state = DailyState(
        user_id=user_id,
        date=today,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    daily_state_repo.get_by_user_and_date.return_value = cached_state

    service = DailyStateService(daily_state_repo, recommendation_repo)
    result = await service.get_daily_state(user_id, today)

    assert result == cached_state
    daily_state_repo.get_by_user_and_date.assert_awaited_with(user_id, today)
    daily_state_repo.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_daily_state_generates_new_if_expired(mock_repos):
    daily_state_repo, recommendation_repo = mock_repos
    user_id = "user1"
    today = datetime.utcnow().date()

    expired_state = DailyState(
        user_id=user_id,
        date=today,
        expires_at=datetime.utcnow() - timedelta(hours=1)
    )
    daily_state_repo.get_by_user_and_date.return_value = expired_state

    generated_state = DailyState(user_id=user_id, date=today, expires_at=datetime.utcnow() + timedelta(hours=1))
    daily_state_repo.update.return_value = generated_state

    service = DailyStateService(daily_state_repo, recommendation_repo)
    result = await service.get_daily_state(user_id, today)

    assert result == generated_state
    daily_state_repo.update.assert_awaited_once()
    daily_state_repo.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_daily_state_generates_new_if_missing(mock_repos):
    daily_state_repo, recommendation_repo = mock_repos
    user_id = "user2"
    today = datetime.utcnow().date()

    daily_state_repo.get_by_user_and_date.return_value = None

    generated_state = DailyState(user_id=user_id, date=today, expires_at=datetime.utcnow() + timedelta(hours=1))
    daily_state_repo.create.return_value = generated_state

    service = DailyStateService(daily_state_repo, recommendation_repo)
    result = await service.get_daily_state(user_id, today)

    assert result == generated_state
    daily_state_repo.create.assert_awaited_once()
    daily_state_repo.update.assert_not_awaited()