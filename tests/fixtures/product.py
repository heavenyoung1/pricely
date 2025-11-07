import pytest
from pydantic import HttpUrl

from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct


@pytest.fixture
def product():
    """Фикстура тестового доменного Product"""
    return Product(
        id="816992280",
        user_id="5702092394",
        name="Рюкзак мужской городской спортивный",
        link="https://www.ozon.ru/product/ryukzak-muzhskoy-gorodskoy-sportivnyy-tevin-816992280/",
    )


@pytest.fixture
def orm_product():
    """Фикстура тестового ORMProduct"""
    return ORMProduct(
        id="816992280",
        name="Рюкзак мужской городской спортивный",
        link="https://www.ozon.ru/product/ryukzak-muzhskoy-gorodskoy-sportivnyy-tevin-816992280/",
    )
