import pytest
from unittest.mock import MagicMock
from src.domain.entities import Product, User
from src.infrastructure.database.core import get_db_session
from src.application.exceptions import UserCreationError

def test_with_uow_commit(mock_product_service, mock_uow, user, mocker):
    """Тест декоратора with_uow с commit=True."""
    # Настраиваем моки
    mock_session = MagicMock()
    mock_user_repo = MagicMock()
    mock_user_repo.get.return_value = None
    mock_user_repo.save.return_value = None
    mocker.patch('src.infrastructure.database.core.get_db_session', return_value=mock_session)
    mocker.patch.object(mock_uow, 'user_repository', return_value=mock_user_repo)
    mocker.patch.object(mock_uow, '__enter__', return_value=mock_uow)
    mocker.patch.object(mock_uow, '__exit__', return_value=None)
    mocker.patch.object(mock_uow, 'commit', return_value=None)
    # Замокаем метод create_user
    mock_product_service.create_user = MagicMock()

    # Выполняем метод с декоратором commit=True
    mock_product_service.create_user(user, uow=mock_uow)

    # Проверяем вызовы
    print(f"get_db_session calls: {get_db_session.mock_calls}")
    print(f"uow.__enter__ calls: {mock_uow.__enter__.mock_calls}")
    print(f"uow.__exit__ calls: {mock_uow.__exit__.mock_calls}")
    print(f"uow.commit calls: {mock_uow.commit.mock_calls}")
    print(f"user_repo.get calls: {mock_user_repo.get.mock_calls}")
    print(f"user_repo.save calls: {mock_user_repo.save.mock_calls}")
    get_db_session.assert_called_once()
    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    mock_uow.commit.assert_called_once()
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_user_repo.save.assert_called_once_with(user)
    mock_product_service.create_user.assert_called_once_with(user, uow=mock_uow)

def test_with_uow_no_commit(mock_product_service, mock_uow, product, mocker):
    """Тест декоратора with_uow с commit=False."""
    # Настраиваем моки
    mock_session = MagicMock()
    mock_product_repo = MagicMock()
    mock_product_repo.get.return_value = product
    mocker.patch('src.infrastructure.database.core.get_db_session', return_value=mock_session)
    mocker.patch.object(mock_uow, 'product_repository', return_value=mock_product_repo)
    mocker.patch.object(mock_uow, '__enter__', return_value=mock_uow)
    mocker.patch.object(mock_uow, '__exit__', return_value=None)
    mocker.patch.object(mock_uow, 'commit', return_value=None)
    # Замокаем метод get_product
    mock_product_service.get_product = MagicMock(return_value=product)

    # Выполняем метод с декоратором commit=False
    result = mock_product_service.get_product(product.id, uow=mock_uow)

    # Проверяем вызовы и результат
    print(f"get_db_session calls: {get_db_session.mock_calls}")
    print(f"uow.__enter__ calls: {mock_uow.__enter__.mock_calls}")
    print(f"uow.__exit__ calls: {mock_uow.__exit__.mock_calls}")
    print(f"uow.commit calls: {mock_uow.commit.mock_calls}")
    print(f"product_repo.get calls: {mock_product_repo.get.mock_calls}")
    assert result == product
    get_db_session.assert_called_once()
    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    mock_uow.commit.assert_not_called()
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_product_service.get_product.assert_called_once_with(product.id, uow=mock_uow)

def test_with_uow_commit_exception(mock_product_service, mock_uow, user, mocker):
    """Тест декоратора with_uow с commit=True, когда метод выбрасывает исключение."""
    # Настраиваем моки
    mock_session = MagicMock()
    mock_user_repo = MagicMock()
    mock_user_repo.get.side_effect = Exception("DB error")
    mocker.patch('src.infrastructure.database.core.get_db_session', return_value=mock_session)
    mocker.patch.object(mock_uow, 'user_repository', return_value=mock_user_repo)
    mocker.patch.object(mock_uow, '__enter__', return_value=mock_uow)
    mocker.patch.object(mock_uow, '__exit__', return_value=None)
    mocker.patch.object(mock_uow, 'commit', return_value=None)
    # Замокаем метод create_user с исключением
    mock_product_service.create_user = MagicMock(side_effect=UserCreationError("Ошибка создания пользователя: DB error"))

    # Проверяем, что исключение пробрасывается и commit не вызывается
    with pytest.raises(UserCreationError, match="Ошибка создания пользователя: DB error"):
        mock_product_service.create_user(user, uow=mock_uow)

    # Проверяем вызовы
    print(f"get_db_session calls: {get_db_session.mock_calls}")
    print(f"uow.__enter__ calls: {mock_uow.__enter__.mock_calls}")
    print(f"uow.__exit__ calls: {mock_uow.__exit__.mock_calls}")
    print(f"uow.commit calls: {mock_uow.commit.mock_calls}")
    print(f"user_repo.get calls: {mock_user_repo.get.mock_calls}")
    get_db_session.assert_called_once()
    mock_uow.__enter__.assert_called_once()
    mock_uow.__exit__.assert_called_once()
    mock_uow.commit.assert_not_called()
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_product_service.create_user.assert_called_once_with(user, uow=mock_uow)