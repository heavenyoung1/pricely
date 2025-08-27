import pytest
import json
from src.application.use_cases.create_user import CreateUserUseCase, UserCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_create_user_use_case_success(mock_user_repo,  user):
    mock_user_repo.get.return_value = None # Пользователь не существует
    use_case = CreateUserUseCase(user_repo=mock_user_repo)

    # Выполняем создание пользователя
    use_case.execute(user=user)

    # Asserts
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_user_repo.save.assert_called_once_with(user)

def test_create_product_use_case_user_exists(mock_user_repo, user):
    mock_user_repo.get.return_value = user # Пользователь существует
    use_case = CreateUserUseCase(user_repo=mock_user_repo)

    use_case.execute(user)
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_user_repo.save.assert_not_called()