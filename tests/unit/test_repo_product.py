import pytest

from src.infrastructure.database.models import ORMProduct, ORMPrice
from src.infrastructure.database.repositories import ProductRepositoryImpl

import logging
logger = logging.getLogger(__name__)


@pytest.mark.unit
def test_save_product_success(product, mock_session, orm_product):
    '''Тестирование успешного сохранения товара в базе данных.'''
    repo = ProductRepositoryImpl(session=mock_session)
    repo.save(product)
    #mock_session.merge.assert_called_once()

@pytest.mark.unit
def test_get_product_found(mock_session, orm_product, product, orm_price_created_first):
    repo = ProductRepositoryImpl(session=mock_session)
    mock_session.get.return_value = orm_product
    # Настраиваем мок для загрузки цен
    mock_session.query.return_value.filter_by.return_value.all.return_value = [orm_price_created_first]
    result = repo.get(product_id=product.id)
    assert result.id == product.id
    assert len(result.prices) == 1  # Проверяем, что цена загрузилась
    assert result.prices[0].with_card == orm_price_created_first.with_card
    mock_session.get.assert_called_once_with(ORMProduct, product.id)
    mock_session.query.assert_called_once_with(ORMPrice)

@pytest.mark.unit  
def test_get_product_not_found(mock_session):
    repo = ProductRepositoryImpl(session=mock_session)
    mock_session.get.return_value = None
    result = repo.get(product_id='NOTEXIST_ID')
    assert result is None
    mock_session.get.assert_called_once_with(ORMProduct, 'NOTEXIST_ID')

@pytest.mark.unit  
def test_delete_product(mock_session, orm_product, product):
    repo = ProductRepositoryImpl(session=mock_session)

    mock_session.get.return_value = orm_product

    result = repo.delete(product.id)

    assert result is True
    mock_session.get.assert_called_once_with(ORMProduct, product.id)
    mock_session.delete.assert_called_once_with(orm_product)