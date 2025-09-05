import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductCreationError
from src.infrastructure.database.repositories import PriceRepositoryImpl, ProductRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.mappers import ProductMapper, PriceMapper
from src.infrastructure.parsers import OzonParser
import logging
logger = logging.getLogger(__name__)

# @patch('src.application.use_cases.create_product.uuid.uuid4')
# @patch('src.application.use_cases.create_product.datetime')
# def test_create_product_use_case_success(
#         mock_datetime,
#         mock_uuid,
#         mock_parser,
#         mock_product_repo,
#         mock_price_repo,
#         mock_user_repo,
#         product,
#         price,
#         user,
#         mocker,
# ):
#     '''Проверяет успешное создание товара и сохранение пользователя, если он не существует.'''
#     # Настраиваем моки
#     mock_uuid.return_value = "pr1"
#     mock_datetime.now.return_value = datetime(2025, 1, 1, 0, 0)
#     mocker.patch.object(mock_user_repo, 'get', return_value=None)  # Пользователь не существует
#     mocker.patch.object(mock_product_repo, 'get', return_value=None)  # Товар не существует
#     mocker.patch.object(mock_product_repo, 'save', return_value=None)
#     mocker.patch.object(mock_price_repo, 'save', return_value=None)
#     mocker.patch.object(mock_user_repo, 'save', return_value=None)
#     mock_parser.parse_product.return_value = {
#         'id': product.id,
#         'name': product.name,
#         'image_url': product.image_url,
#         'rating': product.rating,
#         'categories': product.categories,
#         'price_with_card': price.with_card,
#         'price_without_card': price.without_card,
#         'price_default': price.default,
#     }
#     mocker.patch('src.infrastructure.database.mappers.ProductMapper.domain_to_orm', return_value=ProductMapper.domain_to_orm(product))
#     mocker.patch('src.infrastructure.database.mappers.PriceMapper.domain_to_orm', return_value=PriceMapper.domain_to_orm(price))

#     # Создаем use case
#     use_case = CreateProductUseCase(
#         product_repo=mock_product_repo,
#         price_repo=mock_price_repo,
#         user_repo=mock_user_repo,
#         parser=mock_parser,
#     )

#     # Выполняем создание продукта
#     result = use_case.execute(user_id=user.id, url=product.link)

#     # Проверяем вызовы
#     print(f"mock_user_repo.save call count: {mock_user_repo.save.call_count}")
#     print(f"mock_user_repo.save calls: {mock_user_repo.save.mock_calls}")
#     mock_parser.parse_product.assert_called_once_with(product.link)
#     mock_user_repo.get.assert_called_once_with(user.id)
#     mock_product_repo.get.assert_called_once_with(product.id)
#     mock_product_repo.save.assert_called_once_with(product)
#     mock_price_repo.save.assert_called_once_with(price)
#     mock_user_repo.save.assert_called()
#     assert mock_user_repo.save.call_count == 2  # Два вызова: для нового пользователя и для обновления списка продуктов
#     assert result == {
#         'id': product.id,
#         'name': product.name,
#         'user_id': product.user_id,
#         'price_id': product.price_id
#     }

def test_create_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    user,
    product
        ):
    
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )
    result = use_case.execute(user_id=user.id, url='https://example.com/product')
    logger.debug(f'RESULT USE CASE -> {result}')