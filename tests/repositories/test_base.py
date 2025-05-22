from unittest.mock import MagicMock

from app.repositories.base import BaseRepository


def test_base_repository_connection_property():
    mock_conn = MagicMock()
    repo = BaseRepository(mock_conn)
    assert repo.connection == mock_conn
