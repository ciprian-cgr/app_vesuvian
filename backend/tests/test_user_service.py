import pytest
from unittest.mock import AsyncMock

from app.domains.users.schemas.user import UserCreate
from app.domains.users.services.user import UserService
from app.domains.users.models.user import User


class DummyRepo:
    def __init__(self):
        self.get_by_email = AsyncMock()
        self.get_by_username = AsyncMock()
        self.create = AsyncMock()


@pytest.mark.asyncio
async def test_create_user_success() -> None:
    repo = DummyRepo()
    repo.get_by_email.return_value = None
    repo.get_by_username.return_value = None
    created = User(
        id="1",
        email="test@example.com",
        username="tester",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
        created_at=None,
        updated_at=None,
        refresh_token_version=0,
    )
    repo.create.return_value = created

    service = UserService(repo)
    user_create = UserCreate(email="test@example.com", username="tester", password="secret")

    result = await service.create_user(user_create)
    assert result.email == "test@example.com"
    repo.create.assert_awaited()


@pytest.mark.asyncio
async def test_create_user_duplicate_email() -> None:
    repo = DummyRepo()
    repo.get_by_email.return_value = User(
        id="1",
        email="test@example.com",
        username="other",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
        created_at=None,
        updated_at=None,
        refresh_token_version=0,
    )

    service = UserService(repo)
    user_create = UserCreate(email="test@example.com", username="tester", password="secret")

    with pytest.raises(Exception):
        await service.create_user(user_create)
