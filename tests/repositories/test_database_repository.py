from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import Column, DateTime, Integer, String

from app.cores.database import Base
from app.repositories.database_repository import DatabaseRepository


class DummyModel(Base):
    __tablename__ = "dummy_model"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    deleted_at = Column(DateTime, nullable=True)


@pytest.mark.asyncio
async def test_create():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    obj_mock = MagicMock(spec=DummyModel)

    session_mock.commit = AsyncMock()
    session_mock.refresh = AsyncMock()

    created_obj = await repo.create(obj_mock)

    session_mock.add.assert_called_once_with(obj_mock)
    session_mock.commit.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(obj_mock)
    assert created_obj == obj_mock


@pytest.mark.asyncio
async def test_update_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    existing_mock = MagicMock(spec=DummyModel)
    existing_mock.deleted_at = None

    # Make repo.get return the existing_mock
    repo.get = AsyncMock(return_value=existing_mock)
    session_mock.commit = AsyncMock()
    session_mock.refresh = AsyncMock()

    update_data = {"field1": "val1", "field2": "val2"}
    updated = await repo.update(pk=123, update_data=update_data)

    repo.get.assert_awaited_once()
    session_mock.commit.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(existing_mock)
    # Ensure that fields were set
    assert existing_mock.field1 == "val1"
    assert existing_mock.field2 == "val2"
    # The returned object is the updated instance
    assert updated == existing_mock


@pytest.mark.asyncio
async def test_update_not_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    # Make get return None
    repo.get = AsyncMock(return_value=None)
    # Should return None, no commit triggered
    updated = await repo.update(pk=999, update_data={"field": "val"})
    assert updated is None
    session_mock.commit.assert_not_called()


@pytest.mark.asyncio
async def test_update_restore_soft_deleted():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    existing_mock = MagicMock(spec=Base)
    existing_mock.deleted_at = datetime.now()  # Soft-deleted

    repo.get = AsyncMock(return_value=existing_mock)
    session_mock.commit = AsyncMock()
    session_mock.refresh = AsyncMock()

    updated = await repo.update(pk=111, update_data={"name": "restored"})
    # Because it was soft-deleted, we expect deleted_at is now None
    assert existing_mock.deleted_at is None
    assert existing_mock.name == "restored"
    session_mock.commit.assert_awaited_once()
    session_mock.refresh.assert_awaited_once_with(existing_mock)
    assert updated == existing_mock


@pytest.mark.asyncio
async def test_get_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    # The session.scalars(query).first() chain
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = "fetched_object"
    session_mock.scalars = AsyncMock(return_value=mock_scalars)

    result = await repo.get(DummyModel.id == 7)
    session_mock.scalars.assert_awaited_once()
    assert result == "fetched_object"


@pytest.mark.asyncio
async def test_get_not_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_scalars = MagicMock()
    mock_scalars.first.return_value = None
    session_mock.scalars = AsyncMock(return_value=mock_scalars)

    result = await repo.get(DummyModel.id == 99)
    assert result is None


@pytest.mark.asyncio
async def test_filter_no_expressions():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = ["obj1", "obj2"]
    session_mock.scalars = AsyncMock(return_value=mock_scalars)

    result = await repo.filter()
    session_mock.scalars.assert_awaited_once()
    assert result == ["obj1", "obj2"]


@pytest.mark.asyncio
async def test_filter_with_expressions_skip_limit():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = ["limited1", "limited2"]
    session_mock.scalars = AsyncMock(return_value=mock_scalars)

    result = await repo.filter(DummyModel.id > 10, skip=5, limit=2)
    session_mock.scalars.assert_awaited_once()
    assert result == ["limited1", "limited2"]


@pytest.mark.asyncio
async def test_count_no_expressions():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    session_mock.scalar = AsyncMock(return_value=42)

    cnt = await repo.count()
    session_mock.scalar.assert_awaited_once()
    assert cnt == 42


@pytest.mark.asyncio
async def test_count_with_expressions():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    session_mock.scalar = AsyncMock(return_value=33)

    cnt = await repo.count(DummyModel.id < 50)
    session_mock.scalar.assert_awaited_once()
    assert cnt == 33


@pytest.mark.asyncio
async def test_soft_delete_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_instance = MagicMock(spec=DummyModel)
    # Make get return an existing record
    repo.get = AsyncMock(return_value=mock_instance)
    session_mock.commit = AsyncMock()

    deleted = await repo.soft_delete(123)
    assert deleted is True
    assert mock_instance.deleted_at is not None
    session_mock.add.assert_called_once_with(mock_instance)
    session_mock.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_soft_delete_not_found():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    repo.get = AsyncMock(return_value=None)

    deleted = await repo.soft_delete(999)
    assert deleted is False
    session_mock.commit.assert_not_called()


@pytest.mark.asyncio
async def test_is_exist_true():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_execute = MagicMock()
    # scalar_one_or_none => not None => True
    mock_execute.scalar_one_or_none.return_value = "some_object"
    session_mock.execute = AsyncMock(return_value=mock_execute)

    exists = await repo.is_exist(DummyModel.id == 7)
    assert exists is True


@pytest.mark.asyncio
async def test_is_exist_false():
    session_mock = MagicMock()
    repo = DatabaseRepository(DummyModel, session_mock)
    mock_execute = MagicMock()
    mock_execute.scalar_one_or_none.return_value = None
    session_mock.execute = AsyncMock(return_value=mock_execute)

    exists = await repo.is_exist(DummyModel.id == 77)
    assert exists is False
