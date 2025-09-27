import pytest
from datetime import datetime

from src.application.dto import PriceDTO
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

@pytest.fixture
def price_dto():
    '''Фикстура тестового Price DTO'''
    return PriceDTO(
        id=None,  # 🔥 None
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        created_at=datetime(2025, 1, 1),  #
    )

@pytest.fixture
def price():
    '''Price для юнит-тестов (ещё не сохранён в БД).'''
    return Price(
        id=None,  # 🔥 None до вставки в БД
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        created_at=datetime(2025, 1, 1),  
    )

@pytest.fixture
def price_second():
    '''Фикстура тестового доменного Price'''
    return Price(
        id=None,  # 🔥 тоже None
        product_id='p1',
        with_card=120,
        without_card=140,
        previous_with_card=100,    
        previous_without_card=120,
        created_at=datetime(2025, 1, 2)
    )

@pytest.fixture
def orm_price():
    '''Фикстура тестового ORM Price'''
    return ORMPrice(
        id=1,  # в БД уже сохранён → id есть
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        created_at=datetime(2025, 1, 1),
    )