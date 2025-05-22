import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import DatabaseSessionManager


@pytest.mark.asyncio
async def test_database_session_manager_init_and_close():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    # Engine should not be None after init
    assert manager._engine is not None, "Engine not initialized"
    await manager.close()
    # Should close the engine without error


@pytest.mark.asyncio
async def test_database_session_manager_close_not_initialized():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    manager._engine = None  # Force uninitialized
    with pytest.raises(Exception) as exc:
        await manager.close()
    assert "not initialized" in str(exc.value)


@pytest.mark.asyncio
async def test_database_session_manager_connect():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    async with manager.connect() as conn:
        # Basic check: connection object is valid
        assert conn is not None
    await manager.close()


@pytest.mark.asyncio
async def test_database_session_manager_connect_not_initialized():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    manager._engine = None  # Force uninitialized
    with pytest.raises(Exception) as exc:
        async with manager.connect():
            pass
    assert "not initialized" in str(exc.value)


@pytest.mark.asyncio
async def test_database_session_manager_session():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    async with manager.session() as s:
        # Basic check: session is valid
        assert isinstance(s, AsyncSession)
    await manager.close()


@pytest.mark.asyncio
async def test_database_session_manager_session_not_initialized():
    manager = DatabaseSessionManager("sqlite+aiosqlite:///:memory:")
    manager._sessionmaker = None  # Force uninitialized
    with pytest.raises(Exception) as exc:
        async with manager.session():
            pass
    assert "not initialized" in str(exc.value)
