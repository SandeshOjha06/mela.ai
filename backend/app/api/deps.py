"""
FastAPI dependency injection utilities.

Provides reusable dependency generators for database sessions
and other shared resources.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async database session for the duration of a request.

    The session is automatically closed when the request completes,
    whether successfully or with an error.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
