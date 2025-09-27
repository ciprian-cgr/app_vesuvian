import sys
import pathlib
import os
import asyncio
import pytest
from datetime import datetime
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Ensure backend project root is on sys.path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app
from app.core.database import get_db, Base
from app.domains.users.schemas.user import User
from app.domains.users.routes.users import get_current_user

# Use a file-based SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override the get_db dependency to use the test database."""
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

async def override_get_current_user() -> User:
    """Override the get_current_user dependency to return a mock user."""
    return User(
        id="test-user-id",
        email="test@example.com",
        username="testuser",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Create database tables before tests and drop them after."""
    # Remove the database file if it exists from a previous run
    if os.path.exists("test.db"):
        os.remove("test.db")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup: remove the database file
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for each test function."""
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async client for making API requests."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as ac:
        yield ac