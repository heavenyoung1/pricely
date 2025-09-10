import pytest
import logging

from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.exceptions import ProductCreationError


logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_create_product_success_new_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    user,
):
    # Setup
    pure_mock_user_repo.get.return_value = None  # New user
    pure_mock_product_repo.get.return_value = None

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(user_id=user.id, url='https://example.com/product')

    assert result["product_id"] == "p1"  # Из фикстуры pure_mock_parser
    assert result["product_name"] == "Test Product"
    assert result["user_id"] == user.id

    pure_mock_parser.parse_product.assert_called_once_with('https://example.com/product')
    pure_mock_user_repo.get.assert_called_once_with(user.id)
    pure_mock_product_repo.get.assert_called_once_with("p1")

    assert pure_mock_user_repo.save.call_count == 1
    assert pure_mock_product_repo.save.call_count == 1 
    pure_mock_price_repo.save.assert_called_once()

@pytest.mark.unit
def test_create_product_success_existing_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    user,
):
    pure_mock_user_repo.get.return_value = user  # Existing
    pure_mock_product_repo.get.return_value = None

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(user_id=user.id, url='https://example.com/product')

    assert result["product_id"] == "p1"
    assert result["product_name"] == "Test Product"
    assert result["user_id"] == user.id

    # ИЗМЕНЕНИЕ: save вызывается только если добавляем новый продукт пользователю
    if "p1" not in user.products:
        pure_mock_user_repo.save.assert_called_once()
    else:
        pure_mock_user_repo.save.assert_not_called()
    
    assert pure_mock_product_repo.save.call_count == 1  # был 2, теперь 1
    pure_mock_price_repo.save.assert_called_once()

@pytest.mark.unit
def test_create_product_fails_product_exists(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    product,
):
    pure_mock_parser.parse_product.return_value = {
        "id": "p1",
        "name": "Test Product",
        "image_url": "https://example.com/image.jpg",
        "rating": 4.5,
        "categories": ["cat1", "cat2"],
        "price_with_card": 100,
        "price_without_card": 120,
        "price_default": 150,
    }
    pure_mock_product_repo.get.return_value = product

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )

    with pytest.raises(ProductCreationError, match="уже существует"):
        use_case.execute(user_id="u1", url="https://example.com/product")

    pure_mock_product_repo.save.assert_not_called()
    pure_mock_price_repo.save.assert_not_called()