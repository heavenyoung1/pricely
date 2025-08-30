import pytest
import json
from datetime import datetime
from unittest.mock import patch, MagicMock
from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper, PriceMapper
from src.infrastructure.database.models import ORMUser
from src.infrastructure.core.ozon_parser import OzonParser
from src.application.exceptions import ProductCreationError


@patch('src.application.use_cases.create_product.uuid.uuid4')  # Патчим UUID
@patch('src.application.use_cases.create_product.datetime')  # Патчим datetime
def test_create_product_use_case_success(
        mock_datetime,
        mock_uuid,
        mock_parser,
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        price,
        user,
        mocker,
):
    '''Проверяет успешное создание товара и сохранение пользователя, если он не существует.'''
    # Настраиваем моки
    mock_uuid.return_value = "pr1"
    mock_datetime.now.return_value = datetime(2025, 1, 1, 0, 0)
    mocker.patch.object(mock_user_repo, 'get', return_value=None)  # Пользователь не существует
    mocker.patch.object(mock_product_repo, 'get', return_value=None)  # Товар не существует
    mocker.patch.object(mock_product_repo, 'save', return_value=None)  # Мокаем save для product_repo
    mocker.patch.object(mock_price_repo, 'save', return_value=None)  # Мокаем save для price_repo
    mocker.patch.object(mock_user_repo, 'save', return_value=None)
    mock_parser.parse_product.return_value = {
        'id': product.id,
        'name': product.name,
        'image_url': product.image_url,
        'rating': product.rating,
        'categories': product.categories,
        'price_with_card': price.with_card,
        'price_without_card': price.without_card,
        'price_default': price.default,
        #'claim': price.claim, нахуа он тут нужен?
    }
    mocker.patch('src.infrastructure.mappers.ProductMapper.domain_to_orm', return_value=ProductMapper.domain_to_orm(product))
    mocker.patch('src.infrastructure.mappers.PriceMapper.domain_to_orm', return_value=PriceMapper.domain_to_orm(price))

    # Создаем use case
    use_case = CreateProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
        parser=mock_parser,
    )

    # Выполняем создание продукта
    result = use_case.execute(user_id=user.id, url=product.link)

# Проверяем вызовы
    mock_parser.parse_product.assert_called_once_with(product.link)
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_product_repo.save.assert_called_once_with(product)
    mock_price_repo.save.assert_called_once_with(price)
    mock_user_repo.save.assert_called()
    assert mock_user_repo.save.call_count == 1  # Два вызова: для нового пользователя и для обновления списка продуктов
    assert result == {
        'id': product.id,
        'name': product.name,
        'user_id': product.user_id,
        'price_id': product.price_id
    }