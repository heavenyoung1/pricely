import pytest
from pytest_mock import mocker
import logging
from unittest.mock import MagicMock
from src.infrastructure.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price
from src.infrastructure.mappers import PriceMapper
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)

def test_save_price_success(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет, что цена сохраняется корректно.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch('src.infrastructure.mappers.PriceMapper.domain_to_orm', return_value=orm_price)
    print(f"Type of mock_price_repo.session.merge in test: {type(mock_price_repo.session.merge)}")
    mock_price_repo.save(price_second)
    mock_price_repo.session.merge.assert_called_once_with(orm_price)

def test_save_price_error(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет обработку ошибки при сохранении цены.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch('src.infrastructure.mappers.PriceMapper.domain_to_orm', return_value=orm_price)
    mocker.patch.object(mock_price_repo.session, 'merge', side_effect=SQLAlchemyError("DB error"))
    with pytest.raises(SQLAlchemyError, match="DB error"):
        mock_price_repo.save(price_second)

def test_get_price_success(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет получение цены по ID.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch.object(mock_price_repo.session, 'get', return_value=orm_price)
    result = mock_price_repo.get(price_second.id)
    mock_price_repo.session.get.assert_called_once_with(ORMPrice, price_second.id)

    

def test_get_prices_by_product(price_repo, price, session):
    '''Проверяет получение списка цен продукта.'''
    price_repo.save(price)
    session.commit()

    prices_product_by_API = price_repo.get_all_prices_by_product(price.product_id)
    assert len(prices_product_by_API) == 1
    assert prices_product_by_API[0].id == price.id
    assert prices_product_by_API[0].claim == price.claim
    
def test_delete_price(price_repo, price, session):
    price_repo.save(price)
    session.commit()

    price_by_API = price_repo.get(price.id)
    assert price_by_API is not None
    assert price_by_API.id == price.id
    assert price_by_API.claim == price.claim
    deleted = price_repo.delete(price_id=price.id)
    session.commit()
    assert deleted is True
    price_by_API = price_repo.get(price.id)
    assert price_by_API is None

