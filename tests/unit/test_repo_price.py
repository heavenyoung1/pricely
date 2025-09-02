import pytest
from pytest_mock import mocker
import logging
from unittest.mock import MagicMock
from src.infrastructure.database.repositories import PriceRepositoryImpl
from src.infrastructure.database.mappers import PriceMapper
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)

def test_save_price_success(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет, что цена сохраняется корректно.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch('src.infrastructure.database.mappers.PriceMapper.domain_to_orm', return_value=orm_price)
    print(f"Type of mock_price_repo.session.merge in test: {type(mock_price_repo.session.merge)}")
    mock_price_repo.save(price_second)
    mock_price_repo.session.merge.assert_called_once_with(orm_price)

def test_save_price_error(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет обработку ошибки при сохранении цены.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch('src.infrastructure.database.mappers.PriceMapper.domain_to_orm', return_value=orm_price)
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

def test_get_price_not_found(mock_price_repo, mock_uow, mocker):
    '''Проверяет, что возвращается None для несуществующей цены.'''
    mock_uow.session = mock_price_repo.session
    mocker.patch.object(mock_price_repo.session, 'get', return_value=None)
    result = mock_price_repo.get("non_existent_id")
    mock_price_repo.session.get.assert_called_once_with(ORMPrice, "non_existent_id")
    assert result is None
    # Не проверяем mock_uow.commit, так как commit не вызывается в get

def test_get_prices_by_product_error(price_second, mock_price_repo, mock_uow, mocker):
    '''Проверяет обработку ошибки при получении цен.'''
    mock_uow.session = mock_price_repo.session
    mocker.patch.object(mock_price_repo.session, 'query', side_effect=SQLAlchemyError("DB error"))
    with pytest.raises(SQLAlchemyError, match="DB error"):
        mock_price_repo.get_all_prices_by_product(price_second.product_id)
    # Не проверяем mock_uow.commit, так как commit не вызывается в get

def test_delete_price_success(mock_price_repo, price_second, mock_uow, mocker):
    '''Проверяет успешное удаление цены.'''
    mock_uow.session = mock_price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    mocker.patch.object(mock_price_repo.session, 'get', return_value=orm_price)
    deleted = mock_price_repo.delete(price_second.id)
    mock_price_repo.session.get.assert_called_once_with(ORMPrice, price_second.id)
    mock_price_repo.session.delete.assert_called_once_with(orm_price)
    assert deleted is True