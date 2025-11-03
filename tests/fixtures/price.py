import pytest
from datetime import datetime

from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice


@pytest.fixture
def price_created_first():
    """Price для юнит-тестов"""
    return Price(
        id=None,
        product_id="816992280",
        with_card=1676,
        without_card=1827,
        previous_with_card=None,
        previous_without_card=None,
        created_at=datetime(2025, 1, 1),
    )


@pytest.fixture
def price_after_checking():
    """Фикстура тестового доменного Price"""
    return Price(
        id=None,  # 🔥 тоже None
        product_id="816992280",
        with_card=1950,
        without_card=1901,
        previous_with_card=1676,
        previous_without_card=1827,
        created_at=datetime(2025, 1, 2),
    )


@pytest.fixture
def orm_price_created_first():
    """Фикстура тестового ORM Price"""
    return ORMPrice(
        id=1,
        product_id="816992280",
        with_card=1676,
        without_card=1827,
        previous_with_card=None,
        previous_without_card=None,
        created_at=datetime(2025, 1, 1),
    )


@pytest.fixture
def orm_price_created_checking():
    """Фикстура тестового ORM Price"""
    return ORMPrice(
        id=1,
        product_id="816992280",
        with_card=1676,
        without_card=1827,
        previous_with_card=1676,
        previous_without_card=1827,
        created_at=datetime(2025, 1, 12),
    )
