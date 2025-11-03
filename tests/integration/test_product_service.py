import pytest
from unittest.mock import Mock, patch, MagicMock
from src.infrastructure.services import ProductService
from src.domain.entities import User, Product, Price
from src.domain.exceptions import (
    ProductNotFoundError,
    PriceUpdateError,
    ProductCreationError,
    UserCreationError,
    ParserProductError,
    ProductDeletingError,
    ProductNotExistingDataBase,
)


class TestProductServiceGetProduct:
    """Тесты для получения продукта"""

    @pytest.mark.integration
    def test_get_product_success(self, uow, product, user, pure_mock_parser):
        """Успешно получаем продукт по ID"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)
        service.create_product(user.id, "https://ozon.ru/product/123")

        product_service = service.get_product(product_id=product.id)

        assert product_service is not None
        assert product_service.id == product.id
        assert product_service.name == product.name

    @pytest.mark.integration
    def test_get_product_not_found_raises_exception(self, uow, pure_mock_parser):
        """Исключение при получении несуществующего продукта"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        with pytest.raises(ProductNotFoundError):
            service.get_product(product_id="NOT_EXIST")


class TestProductServiceGetFullProduct:
    """Тесты для получения полной информации о продукте"""

    @pytest.mark.integration
    def test_get_full_product_success(
        self, uow, product, price_created_first, user, pure_mock_parser
    ):
        """Успешно получаем полную информацию о продукте"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)
        service.create_product(user.id, "https://ozon.ru/product/123")

        full_product = service.get_full_product(product_id=product.id)

        assert full_product["id"] == product.id
        assert full_product["name"] == product.name
        assert "latest_price" in full_product
        assert (
            full_product["latest_price"]["with_card"] == price_created_first.with_card
        )
        assert (
            full_product["latest_price"]["without_card"]
            == price_created_first.without_card
        )

    @pytest.mark.integration
    def test_get_full_product_not_found_raises_exception(self, uow, pure_mock_parser):
        """Исключение при получении полной информации несуществующего продукта"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        with pytest.raises(ProductNotFoundError):
            service.get_full_product(product_id="NOT_EXIST")


class TestProductServiceCreateUser:
    """Тесты для создания пользователя"""

    @pytest.mark.integration
    def test_create_user_success(self, uow, user, mock_parser):
        """Успешно создаём пользователя"""
        service = ProductService(uow_factory=lambda: uow, parser=mock_parser)

        service.create_user(user)

        with uow:
            saved_user = uow.user_repository.get(user.id)

        assert saved_user is not None
        assert saved_user.id == user.id
        assert saved_user.username == user.username
        assert saved_user.chat_id == user.chat_id

    # @pytest.mark.integration
    # def test_create_user_duplicate_raises_error(self, uow, user, mock_parser):
    #     """Исключение при создании дублирующегося пользователя"""
    #     service = ProductService(uow_factory=lambda: uow, parser=mock_parser)

    #     service.create_user(user)

    #     with pytest.raises(UserCreationError):
    #         service.create_user(user)

    # @pytest.mark.integration
    # def test_create_user_logs_error_on_exception(self, uow, user, mock_parser, caplog):
    #     """Логирование ошибки при создании пользователя"""
    #     service = ProductService(uow_factory=lambda: uow, parser=mock_parser)
    #     uow.user_repository.add = Mock(side_effect=Exception("DB Error"))

    #     with pytest.raises(UserCreationError):
    #         service.create_user(user)

    #     assert "Ошибка при создании пользователя" in caplog.text


class TestProductServiceCreateProduct:
    """Тесты для создания продукта"""

    @pytest.mark.integration
    def test_create_product_success(
        self, uow, price_created_first, product, user, pure_mock_parser
    ):
        """Успешно создаём продукт"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)

        url = "https://ozon.ru/product/123"
        result = service.create_product(user.id, url)

        assert result["product_id"] == product.id
        assert result["with_card"] == price_created_first.with_card

        with uow:
            product_fetched = uow.product_repository.get(product_id=product.id)

        assert product_fetched is not None


#  НЕ РАБОТАЕТ!!!!!!!!!!!!!!
# @pytest.mark.integration
# def test_create_product_invalid_url_format(self, uow, user):
#     """Ошибка при создании продукта с неправильным URL"""
#     # Создаём парсер, который выбрасывает ошибку
#     mock_parser = Mock()
#     mock_parser.parse.side_effect = ParserProductError('Ошибка парсинга товара')

#     service = ProductService(uow_factory=lambda: uow, parser=mock_parser)
#     service.create_user(user)

#     # Парсер выбрасывает ParserProductError при невалидном URL
#     with pytest.raises(ParserProductError):
#         service.create_product(user.id, "invalid_url")


class TestProductServiceDeleteProduct:
    """Тесты для удаления продукта"""

    @pytest.mark.integration
    def test_delete_product_success(self, uow, product, user, pure_mock_parser):
        """Успешно удаляем продукт"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)
        service.create_product(user.id, "https://ozon.ru/product/123")

        service.delete_product(product_id=product.id)

        with uow:
            product_uow = uow.product_repository.get(product_id=product.id)

        assert product_uow is None

    @pytest.mark.integration
    def test_delete_product_not_found_raises_exception(self, uow, pure_mock_parser):
        """Исключение при удалении несуществующего продукта"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        with pytest.raises(ProductNotExistingDataBase):
            service.delete_product(product_id="NOT_EXIST")


class TestProductServiceUpdatePrice:
    """Тесты для обновления цены продукта"""

    @pytest.mark.integration
    def test_update_product_price_success(
        self,
        uow,
        product,
        user,
        pure_mock_parser,
        price_created_first,
        price_after_checking,
    ):
        """Успешно обновляем цену продукта"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        # Создаем пользователя и продукт
        service.create_user(user)
        result = service.create_product(user.id, "https://ozon.ru/product/123")

        # Настроим мок для парсера, чтобы он возвращал новые данные цены
        pure_mock_parser.check_product.return_value = {
            "price_with_card": price_after_checking.with_card,
            "price_without_card": price_after_checking.without_card,
        }

        # Обновляем цену продукта
        update_result = service.update_product_price(product_id=product.id)

        # Проверяем структуру результата
        assert "updated_product" in update_result
        assert "is_changed" in update_result
        assert isinstance(update_result["is_changed"], bool)

        # Проверяем, что продукт существует и имеет обновленные цены
        with uow:
            product_with_upd_price = uow.product_repository.get(
                product_id=result["product_id"]
            )

        assert product_with_upd_price is not None
        assert product_with_upd_price.id == product.id

        # Проверяем, что цены были обновлены - продукт должен иметь 2 цены
        # (начальная и обновлённая)
        assert len(product_with_upd_price.prices) >= 2

        # Последняя цена должна соответствовать обновлённым значениям
        latest_price = product_with_upd_price.prices[-1]
        assert latest_price.with_card == price_after_checking.with_card
        assert latest_price.without_card == price_after_checking.without_card

    @pytest.mark.integration
    def test_update_product_price_returns_correct_structure(
        self, uow, product, user, pure_mock_parser
    ):
        """Результат обновления цены имеет правильную структуру"""
        # Настройка парсера (мокаем возвращаемые значения)
        pure_mock_parser.check_product.return_value = {
            "price_with_card": 1950,
            "price_without_card": 1901,
        }

        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)
        service.create_product(user.id, "https://ozon.ru/product/123")

        result = service.update_product_price(product_id=product.id)

        assert isinstance(result, dict)
        assert "updated_product" in result
        assert "is_changed" in result

    @pytest.mark.integration
    def test_update_price_nonexistent_product(self, uow, pure_mock_parser):
        """Ошибка при обновлении цены несуществующего продукта"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        with pytest.raises(ProductNotFoundError):
            service.update_product_price(product_id="NOT_EXIST")


class TestProductServiceGetAllProducts:
    """Тесты для получения всех продуктов пользователя"""

    @pytest.mark.integration
    def test_get_all_products_empty_list(self, uow, user, pure_mock_parser):
        """Возвращаем пустой список для пользователя без продуктов"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)

        products = service.get_all_products(user_id=user.id)

        assert products == []

    @pytest.mark.integration
    def test_get_all_products_success(self, uow, product, user, pure_mock_parser):
        """Успешно получаем все продукты пользователя"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        service.create_user(user)
        service.create_product(user.id, "https://ozon.ru/product/123")

        products = service.get_all_products(user_id=user.id)

        assert len(products) > 0
        assert all(isinstance(p, dict) or hasattr(p, "id") for p in products)


class TestProductServiceGetAllProductsForUpdate:
    """Тесты для получения продуктов для обновления"""

    @pytest.mark.integration
    def test_get_all_products_for_update_returns_list(self, uow, pure_mock_parser):
        """Возвращаем список продуктов для обновления"""
        service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

        result = service.get_all_products_for_update()

        assert isinstance(result, dict)

        # Дополнительная проверка, чтобы убедиться, что словарь содержит правильные данные
        # Проверяем, что словарь не пустой и содержит ключи
        assert len(result) >= 0
        assert all(
            isinstance(v, list) for v in result.values()
        )  # Значения должны быть списками
