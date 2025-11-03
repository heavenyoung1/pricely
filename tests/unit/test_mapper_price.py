import pytest
from src.infrastructure.database.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice


@pytest.mark.unit
def test_domain_to_orm_with_valid_data(price_created_first):
    """
    Тестирование преобразования доменной модели в ORM модель
    с валидными данными.
    """
    orm_price = PriceMapper.domain_to_orm(price_created_first)

    # Проверяем тип данных
    assert isinstance(orm_price, ORMPrice)

    # Проверяем, что данные маппятся корректно
    assert_prices_equal(orm_price, price_created_first)

    # Проверяем, что id остается пустым
    assert orm_price.id is None


@pytest.mark.unit
def test_orm_to_domain_with_valid_data(orm_price_created_first):
    """
    Тестирование преобразования ORM модели в доменную модель
    с валидными данными.
    """
    domain_price = PriceMapper.orm_to_domain(orm_price_created_first)

    # Проверяем тип данных
    assert isinstance(domain_price, Price)

    # Проверяем, что данные маппятся корректно
    assert_prices_equal(orm_price_created_first, domain_price)


@pytest.mark.unit
def test_domain_to_orm_with_some_changes(price_after_checking):
    """
    Тестирование преобразования доменной модели в ORM модель
    с измененными данными.
    """
    orm_price = PriceMapper.domain_to_orm(price_after_checking)

    # Проверяем тип данных
    assert isinstance(orm_price, ORMPrice)

    # Проверяем, что данные маппятся корректно
    assert_prices_equal(orm_price, price_after_checking)


@pytest.mark.unit
def test_orm_to_domain_with_some_changes(orm_price_created_checking):
    """
    Тестирование преобразования ORM модели в доменную модель
    с измененными данными.
    """
    domain_price = PriceMapper.orm_to_domain(orm_price_created_checking)

    # Проверяем тип данных
    assert isinstance(domain_price, Price)

    # Проверяем, что данные маппятся корректно
    assert_prices_equal(orm_price_created_checking, domain_price)


# Универсальная функция для проверки совпадения всех полей
def assert_prices_equal(orm_price, domain_price):
    assert orm_price.product_id == domain_price.product_id
    assert orm_price.with_card == domain_price.with_card
    assert orm_price.without_card == domain_price.without_card
    assert orm_price.previous_with_card == domain_price.previous_with_card
    assert orm_price.previous_without_card == domain_price.previous_without_card
    assert orm_price.created_at == domain_price.created_at
