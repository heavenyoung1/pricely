import pytest
from unittest.mock import MagicMock
from src.application.use_cases import GetUserProductsUseCase


@pytest.mark.unit
def test_get_user_products_success(pure_mock_user_products_repo):
    # Настроим мок для репозитория
    mock_data = [
        {"user_id": "user1", "product_id": "product1"},
        {"user_id": "user2", "product_id": "product2"},
        {"user_id": "user3", "product_id": "product3"},
    ]
    # Мокируем метод get_sorted_user_products для возврата тестовых данных
    pure_mock_user_products_repo.get_sorted_user_products.return_value = mock_data

    # Создаем UseCase
    use_case = GetUserProductsUseCase(user_products_repo=pure_mock_user_products_repo)

    # Вызов метода
    result = use_case.execute()

    # Проверяем, что результат соответствует тестовым данным
    assert result == mock_data

    # Проверяем, что метод репозитория был вызван
    pure_mock_user_products_repo.get_sorted_user_products.assert_called_once()
