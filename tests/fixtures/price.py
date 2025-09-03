import pytest
from datetime import datetime

from src.application.dto import PriceDTO
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

@pytest.fixture
def price_dto():
    '''Фикстура тестового Price DTO'''
    return PriceDTO(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )

@pytest.fixture
def price():
    '''Фикстура тестового доменного Price'''
    return Price(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=None,        #90
        previous_without_card=None,     #110,
        default=150,
        claim=datetime(2025, 1, 1)
    )

@pytest.fixture
def price_second():
    '''Фикстура тестового доменного Price'''
    return Price(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,    
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )

@pytest.fixture
def orm_price(db_session):
    '''Фикстура тестового ORM Price'''
    price = ORMPrice(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )
    db_session.add(price)
    db_session.commit()
    return price

@pytest.fixture
def mocked_orm_price():
    '''Фикстура ORMPrice без взаимодействия с БД (для unit-тестов).'''
    price = ORMPrice(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )
    return price