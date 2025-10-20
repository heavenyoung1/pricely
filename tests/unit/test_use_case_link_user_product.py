import pytest
from unittest.mock import MagicMock
from src.application.use_cases.link_user_product import LinkUserProductUseCase

@pytest.mark.unit
def test_link_user_product_success(pure_mock_user_products_repo):
    '''Тест успешного создания связи между пользователем и продуктом.'''

    # Данные для теста
    user_id = "12345"
    product_id = "67890"

    # Настроим мок репозитория, чтобы возвращать пустой список (связи нет)
    pure_mock_user_products_repo.get_products_for_user.return_value = []

    # Создаем UseCase
    use_case = LinkUserProductUseCase(user_products_repo=pure_mock_user_products_repo)

    # Вызов метода
    use_case.execute(user_id=user_id, product_id=product_id)

    # Проверяем, что метод add_product_for_user был вызван с правильными параметрами
    pure_mock_user_products_repo.add_product_for_user.assert_called_once_with(user_id, product_id)

    # Проверяем, что не было попытки добавления повторной связи
    pure_mock_user_products_repo.get_products_for_user.assert_called_once_with(user_id)


@pytest.mark.unit
def test_link_user_product_already_exists(pure_mock_user_products_repo):
    '''Тест, когда связь между пользователем и продуктом уже существует.'''

    # Данные для теста
    user_id = "12345"
    product_id = "67890"

    # Настроим мок репозитория, чтобы возвращать список с уже существующей связью
    pure_mock_user_products_repo.get_products_for_user.return_value = [{'product_id': product_id}]

    # Создаем UseCase
    use_case = LinkUserProductUseCase(user_products_repo=pure_mock_user_products_repo)

    # Вызов метода
    use_case.execute(user_id=user_id, product_id=product_id)

    # Проверяем, что метод add_product_for_user не был вызван (связь уже существует)
    pure_mock_user_products_repo.add_product_for_user.assert_not_called()

    # Проверяем, что get_products_for_user был вызван только один раз
    pure_mock_user_products_repo.get_products_for_user.assert_called_once_with(user_id)
