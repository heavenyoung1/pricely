import pytest
from unittest.mock import MagicMock
from src.application.use_cases import GetUserUseCase
from src.domain.entities import User
from src.domain.exceptions import UserNotFoundError

@pytest.mark.unit
def test_get_user_success(pure_mock_user_repo):
    # Настроим мок репозитория, чтобы он возвращал тестового пользователя
    user_id = "12345"
    mock_user = User(id=user_id, username="testuser", chat_id="98765", products=[])
    pure_mock_user_repo.get.return_value = mock_user

    # Создаем UseCase
    use_case = GetUserUseCase(user_repo=pure_mock_user_repo)

    # Вызов метода
    result = use_case.execute(user_id=user_id)

    # Проверяем, что результат соответствует ожидаемому пользователю
    assert result.id == mock_user.id
    assert result.username == mock_user.username
    assert result.chat_id == mock_user.chat_id
    assert result.products == mock_user.products

    # Проверяем, что метод get был вызван с нужным user_id
    pure_mock_user_repo.get.assert_called_once_with(user_id)


@pytest.mark.unit
def test_get_user_not_found(pure_mock_user_repo):
    # Настроим мок репозитория, чтобы он вернул None, имитируя отсутствие пользователя
    user_id = "12345"
    pure_mock_user_repo.get.return_value = None

    # Создаем UseCase
    use_case = GetUserUseCase(user_repo=pure_mock_user_repo)

    # Проверяем, что метод выбрасывает исключение
    with pytest.raises(UserNotFoundError, match=f'Пользователь с ID {user_id} не найден'):
        use_case.execute(user_id=user_id)

    # Проверяем, что метод get был вызван с нужным user_id
    pure_mock_user_repo.get.assert_called_once_with(user_id)
