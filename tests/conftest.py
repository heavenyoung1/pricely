import logging
import pytest
from datetime import datetime
from typing import Generator, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.database.models.base import Base
from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository


def pytest_configure(config) -> None:
    '''
    Конфигурация pytest:
    Устанавливает базовый формат логирования для всех тестов.
    Уровень логирования — INFO, выводится время, имя логгера, уровень и сообщение.
    '''
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@pytest.fixture
def product_test() -> Dict[str, object]:
    '''
    Возвращает словарь с тестовыми данными для продукта.
    Используется для инициализации экземпляра доменной сущности Product.
    '''
    return {
        'product_id': '1804652778',  # Было 'id'
        'user_id': '0000000000',
        'name': 'Чаша для кальяна глиняная',
        'rating': 4.9,
        'price_with_card': 500,
        'price_without_card': 561,
        'previous_price_with_card': 600,
        'previous_price_without_card': 600,
        'price_default': 899,
        # 'discount_amount': float,
        'link': 'https://www.ozon.ru/product/chasha-dlya-kalyana-glinyanaya-cosmo-bowl-turkish-shot-1804652778/',
        'url_image': 'https://ir.ozone.ru/s3/multimedia-1-9/wc1000/7352613513.jpg',
        'category_product': [
            'Товары для курения и аксессуары',
            'Товары для курения',
            'Аксессуары и комплектующие для кальянов',
            'Комплектующие',
            'Cosmo Bowl',
        ],
        'last_timestamp': datetime(2025, 1, 1, 1, 2, 3),  # Было 'timestamp'
    }

@pytest.fixture
def product(product_test: Dict[str, object]) -> Product:
    '''
    Возвращает экземпляр доменной сущности Product,
    инициализированный данными из фикстуры product_test.
    '''
    return Product(**product_test)

@pytest.fixture
def price_stamp() -> PriceStamp:
    '''
    Возвращает экземпляр доменной сущности PriceStamp
    с тестовыми значениями. Используется в тестах, связанных с ценами продукта.
    '''
    return PriceStamp(
        ID_stamp='stamp1',  # Использую str, чтобы соответствовать DBPriceStamp
        ID_product='1804652778',
        time_stamp=datetime(2025, 1, 1, 1, 2, 3),
        price_with_card=500,
        price_without_card=561,
        previous_price_with_card=600,
        previous_price_without_card=600,
        price_default=899,
    )

@pytest.fixture
def price_stamps() -> list[PriceStamp]:
    return [
        PriceStamp(
            ID_stamp='stamp1',
            ID_product='1804652778',
            time_stamp=datetime(2025, 1, 1, 1, 2, 3),
            price_with_card=500,
            price_without_card=561,
            previous_price_with_card=600,
            previous_price_without_card=600,
            price_default=899,
        ),
        PriceStamp(
            ID_stamp='stamp2',
            ID_product='1804652779',
            time_stamp=datetime(2025, 1, 1, 1, 2, 4),
            price_with_card=600,
            price_without_card=661,
            previous_price_with_card=700,
            previous_price_without_card=700,
            price_default=999,
        ),
    ]

@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    '''
    Создаёт временную in-memory SQLite базу данных и возвращает SQLAlchemy-сессию.
    Используется для изолированного тестирования, не требующего подключения к реальной БД.

    После завершения теста:
    - транзакция откатывается,
    - таблицы удаляются,
    - соединение закрывается.
    '''
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)
    session.close()

@pytest.fixture
def repo(db_session: Session) -> PGSQLProductRepository:
    '''
    Возвращает экземпляр репозитория PGSQLProductRepository,
    инициализированный сессией к временной in-memory базe данных.
    '''
    return PGSQLProductRepository(db_session)