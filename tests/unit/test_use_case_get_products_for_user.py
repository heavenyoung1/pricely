import pytest

from src.application.use_cases import GetProductForUserUseCase

@pytest.mark.unit
def test_get_product_for_user_success(
    pure_mock_user_products_repo,
    pure_mock_product_repo,
    pure_mock_price_repo,
    product,
):
    # Настройка мока для репозитория привязки товаров и пользователей
    pure_mock_user_products_repo.get_products_for_user.return_value = [product.id]

    # Создаем UseCase
    use_case = GetProductForUserUseCase(
        user_products_repo=pure_mock_user_products_repo,
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
    )  

    # Вызов метода
    result = use_case.execute(user_id="user_123")

    # Проверяем, что метод для получения товаров был вызван один раз
    pure_mock_user_products_repo.get_products_for_user.assert_called_once_with("user_123")
    pure_mock_product_repo.get.assert_not_called()  # Не должны были запрашиваться подробности о товарах

@pytest.mark.unit
def test_get_product_for_user_no_products(
    pure_mock_user_products_repo,
    pure_mock_product_repo,
    pure_mock_price_repo,
):
    # Настройка мока для репозитория привязки товаров и пользователей
    pure_mock_user_products_repo.get_products_for_user.return_value = []

    # Создаем UseCase
    use_case = GetProductForUserUseCase(
        user_products_repo=pure_mock_user_products_repo,
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
    )  

    # Вызов метода
    result = use_case.execute(user_id="user_123")

    # Проверяем, что метод для получения товаров был вызван один раз
    pure_mock_user_products_repo.get_products_for_user.assert_called_once_with("user_123")
    pure_mock_product_repo.get.assert_not_called()  # Не должны были запрашиваться подробности о товарах

    # Проверяем, что возвращается пустой список, так как товаров нет
    assert result == []