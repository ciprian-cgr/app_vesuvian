"""
Database configuration and session management.
"""
from functools import lru_cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings, Settings

settings: Settings = get_settings()


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


@lru_cache()
def get_engine() -> AsyncEngine:
    """Create and cache the async engine. This is lazy to avoid
    importing DB driver modules at module import time.
    """
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
    )


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """Return an async session factory bound to the cached engine."""
    engine = get_engine()
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session.

    Yields an AsyncSession. Uses the async context manager which will
    close the session automatically on exit.
    """
    session_maker = get_sessionmaker()
    async with session_maker() as session:
        yield session


async def create_tables() -> None:
    """Create database tables using the engine returned by get_engine()."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
