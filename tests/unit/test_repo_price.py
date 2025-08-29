import pytest
from pytest_mock import mocker
import logging
from unittest.mock import MagicMock
from src.infrastructure.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price
from src.infrastructure.mappers import PriceMapper


logger = logging.getLogger(__name__)

def test_save_price_success(price_second, price_repo, mock_uow, mocker):
    '''Проверяет, что цена сохраняется корректно.'''
    mocker.patch.object(price_repo.session, 'merge', MagicMock())
    mock_uow.session = price_repo.session
    orm_price = PriceMapper.domain_to_orm(price_second)
    #mocker.patch('src.infrastructure.mappers.PriceMapper.domain_to_orm', return_value=orm_price)
    print(f"Type of price_repo.session.merge after patch: {type(price_repo.session.merge)}")
    price_repo.save(price_second)
    price_repo.session.merge.assert_called_once_with(orm_price)



def test_get_price(price_repo, price, session):
    '''Проверяет, что метод репозитория get корректно возвращает цену.'''
    price_repo.save(price)
    session.commit()

    orm_price_by_BD = session.get(ORMPrice, price.id)
    price_by_bd = PriceMapper.orm_to_domain(orm_price_by_BD)
    price_by_API = price_repo.get(price.id)
    assert price_by_bd.id == price.id
    assert price_by_API.id == price.id

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

