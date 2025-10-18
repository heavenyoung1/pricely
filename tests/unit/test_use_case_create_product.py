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
    pure_mock_user_products_repo,
    pure_mock_parser,
    product,
    user,
):
    # Setup
    pure_mock_user_repo.get.return_value = None 
    pure_mock_product_repo.get.return_value = None

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        user_products_repo=pure_mock_user_products_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(user_id=user.id, url='https://example.com/product')

    assert result["product_id"] == product.id  # Из фикстуры pure_mock_parser
    assert result["product_name"] == product.name
    assert result["user_id"] == user.id

    pure_mock_parser.parse_product.assert_called_once_with('https://example.com/product')
    pure_mock_user_repo.get.assert_called_once_with(user.id)
    pure_mock_product_repo.get.assert_called_once_with(product.id)

    assert pure_mock_user_repo.save.call_count == 1
    assert pure_mock_product_repo.save.call_count == 1 
    pure_mock_price_repo.save.assert_called_once()

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
    
    result = use_case.execute(user_id=user.id, url='https://example.com/product')

    assert result["product_id"] == product.id
    assert result["product_name"] == product.name
    assert result["user_id"] == user.id

    # Проверяем, что save для продукта и цены все же был вызван
    pure_mock_product_repo.save.assert_called_once()
    pure_mock_price_repo.save.assert_called_once()
    pure_mock_user_repo.save.assert_called_once()

# @pytest.mark.unit
# def test_create_product_fails_product_exists(
#     pure_mock_product_repo,
#     pure_mock_price_repo,
#     pure_mock_user_repo,
#     pure_mock_user_products_repo,
#     pure_mock_parser,
#     product,
# ):
#     pure_mock_parser.parse_product.return_value = {
#         "id": "816992280",
#         "name": "Test Product",
#         "image_url": "https://example.com/image.jpg",
#         "rating": 4.5,
#         "categories": ["cat1", "cat2"],
#         "price_with_card": 100,
#         "price_without_card": 120,
#     }
#     pure_mock_product_repo.get.return_value = product

#     use_case = CreateProductUseCase(
#         product_repo=pure_mock_product_repo,
#         price_repo=pure_mock_price_repo,
#         user_repo=pure_mock_user_repo,
#         parser=pure_mock_parser,
#         user_products_repo=pure_mock_user_products_repo,
#     )

#     with pytest.raises(ProductCreationError, match="уже существует"):
#         use_case.execute(user_id="u1", url="https://example.com/product")

#     pure_mock_product_repo.save.assert_not_called()
#     pure_mock_price_repo.save.assert_not_called()