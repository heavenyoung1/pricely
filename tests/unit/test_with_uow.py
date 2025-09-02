import pytest
from unittest.mock import MagicMock
from src.domain.entities import Product, User
from src.infrastructure.database.core import get_db_session, with_uow
from src.infrastructure.database.core.unit_of_work import UnitOfWork
from src.domain.exceptions import UserCreationError

def test_with_uow_commit_true(mocker):
    """Проверяет что при commit=True вызывается commit и закрывается сессия."""
    # Мокаем сессию
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.close = MagicMock()

    # Мокаем get_db_session
    mock_get_db_session = mocker.patch(
        "src.infrastructure.database.core.database.get_db_session",
        return_value=mock_session,
    )

    # Тестовая функция под декоратором
    @with_uow(commit=True)
    def foo(uow: UnitOfWork):
        assert isinstance(uow, UnitOfWork)
        return "ok"

    result = foo()

    assert result == "ok"
    mock_get_db_session.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()


def test_with_uow_commit_false(mocker):
    """Проверяет что при commit=False commit не вызывается."""
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.close = MagicMock()

    mock_get_db_session = mocker.patch(
        "src.infrastructure.database.core.database.get_db_session",
        return_value=mock_session,
    )

    @with_uow(commit=False)
    def foo(uow: UnitOfWork):
        return "bar"

    result = foo()

    assert result == "bar"
    mock_get_db_session.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.close.assert_called_once()


def test_with_uow_raises_and_rollback(mocker):
    """Проверяет что при исключении вызывается rollback."""
    mock_session = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.rollback = MagicMock()
    mock_session.close = MagicMock()

    mock_get_db_session = mocker.patch(
        "src.infrastructure.database.core.database.get_db_session",
        return_value=mock_session,
    )

    @with_uow(commit=True)
    def foo(uow: UnitOfWork):
        raise ValueError("boom")

    with pytest.raises(ValueError):
        foo()

    mock_get_db_session.assert_called_once()
    mock_session.rollback.assert_called_once()
    mock_session.commit.assert_not_called()
    mock_session.close.assert_called_once()