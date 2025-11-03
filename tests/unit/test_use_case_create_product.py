import pytest
import logging

from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.exceptions import ProductCreationError, ParserProductError
from src.application.use_cases.create_product import is_url, exctract_link


logger = logging.getLogger(__name__)


@pytest.mark.unit
def test_create_product_success_new_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
    user,
):
    # Arrange
    pure_mock_user_repo.get.return_value = None  # Новый пользователь
    pure_mock_product_repo.get.return_value = None  # Новый товар

    # Act
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        user_products_repo=pure_mock_user_products_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(user_id=user.id, url="https://example.com/product")

    assert result["product_id"] == product.id  # Из фикстуры pure_mock_parser
    assert result["product_name"] == product.name
    assert result["user_id"] == user.id

    # Assert
    pure_mock_parser.parse_product.assert_called_once_with(
        "https://example.com/product"
    )
    pure_mock_user_repo.get.assert_called_once_with(user.id)
    pure_mock_product_repo.get.assert_called_once_with(product.id)

    assert pure_mock_product_repo.save.call_count == 1
    pure_mock_price_repo.save.assert_called_once()
    assert pure_mock_user_repo.save.call_count == 1


@pytest.mark.unit
def test_create_product_success_existing_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
    user,
):
    # Настроим mock для существующего пользователя
    pure_mock_user_repo.get.return_value = user  # Пользователь существует
    pure_mock_product_repo.get.return_value = None  # Товар в базе данных не найден

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
        user_products_repo=pure_mock_user_products_repo,
    )

    result = use_case.execute(user_id=user.id, url="https://example.com/product")

    assert result["product_id"] == product.id
    assert result["product_name"] == product.name
    assert result["user_id"] == user.id

    # Проверяем, что save для продукта и цены все же был вызван
    pure_mock_product_repo.save.assert_called_once()
    pure_mock_price_repo.save.assert_called_once()
    pure_mock_user_repo.save.assert_called_once()

    # Проверяем, что товар был добавлен в список продуктов пользователя
    assert product.id in user.products


@pytest.mark.unit
def test_create_product_fails_product_exists(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    parser_data,
    product,
):
    # Arrange
    pure_mock_product_repo.get.return_value = product  # Товар уже существует

    # Act
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
        user_products_repo=pure_mock_user_products_repo,
    )

    # Assert
    with pytest.raises(
        ProductCreationError, match="Товар с ID 816992280 уже существует"
    ):
        use_case.execute(user_id="u1", url="https://example.com/product")

    pure_mock_product_repo.save.assert_not_called()
    pure_mock_price_repo.save.assert_not_called()
    pure_mock_user_repo.save.assert_not_called()


@pytest.mark.unit
def test_create_product_fails_parsing_error(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
):
    # Настроим mock для парсера, чтобы он выбрасывал ошибку
    pure_mock_parser.parse_product.side_effect = Exception("Ошибка парсинга URL")

    # Act & Assert
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
        user_products_repo=pure_mock_user_products_repo,
    )
    with pytest.raises(ParserProductError, match="Ошибка парсинга товара"):
        use_case.execute(user_id="635777007", url="https://example.com/product")

    pure_mock_product_repo.save.assert_not_called()
    pure_mock_price_repo.save.assert_not_called()


@pytest.mark.unit
def test_create_product_fails_save_error(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
    user,
):
    pure_mock_product_repo.get.return_value = product
    pure_mock_user_repo.get.return_value = None

    pure_mock_product_repo.save.side_effect = ProductCreationError(
        "Ошибка сохранения товара"
    )
    # Act
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
        user_products_repo=pure_mock_user_products_repo,
    )

    # Assert
    with pytest.raises(
        ProductCreationError, match="Товар с ID 816992280 уже существует"
    ):
        use_case.execute(user_id="635777007", url="https://example.com/product")

    pure_mock_product_repo.save.assert_not_called()
    pure_mock_price_repo.save.assert_not_called()


@pytest.mark.unit
def test_create_product_fails_save_error(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
    user,
):
    # Настроим mock для метода save, чтобы он выбрасывал исключение
    pure_mock_product_repo.get.return_value = None  # Продукта нет в БД
    pure_mock_user_repo.get.return_value = user  # Пользователь существует
    pure_mock_product_repo.save.side_effect = ProductCreationError(
        "Ошибка сохранения товара"
    )

    # Создаем use case
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
        user_products_repo=pure_mock_user_products_repo,
    )

    # Проверяем, что при попытке выполнить create_product будет выброшено исключение
    with pytest.raises(ProductCreationError, match="Ошибка сохранения товара"):
        use_case.execute(user_id=user.id, url="https://example.com/product")


@pytest.mark.unit
def test_is_url():
    # Положительные тесты
    assert is_url("https://example.com") == True
    assert is_url("Книга") == False


@pytest.mark.unit
def test_exctract_link():
    assert exctract_link("https://example.com") == "https://example.com"
    assert (
        exctract_link("Книга художественная https://example.com")
        == "https://example.com"
    )
