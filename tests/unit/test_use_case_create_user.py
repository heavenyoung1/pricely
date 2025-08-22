import pytest
import json
from src.application.use_cases.create_user import CreateUserUseCase, UserCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_create_user_use_case_success(
        mock_user_repo,  
        user,
    ):

    # Настраиваем моки
    mock_user_repo.get.return_value = None      # Пользователь НЕ существует

    # Создаём use case
    use_case = CreateUserUseCase(user_repo=mock_user_repo)

    # Выполняем создание продукта
    use_case.execute(user=user)

    # Assert
    mock_user_repo.save.assert_called_once_with(user)

def test_create_product_use_case_user_exists(
        mock_user_repo,  
        user,
    ):
    '''Юнит-тест: ошибка, если пользователь уже существует.'''
    # Настраиваем моки
    mock_user_repo.get.return_value = user      # Пользователь существует

    # Создаём use case
    use_case = CreateUserUseCase(user_repo=mock_user_repo)

    # Выполняем создание пользователя
    with pytest.raises(UserCreationError, match=f'Пользователь {user.id} уже существует'):
        use_case.execute(user=user)