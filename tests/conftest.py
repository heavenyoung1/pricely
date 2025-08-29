import pytest
import logging
import json
import sys
from datetime import datetime
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.infrastructure.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.models import Base, ORMProduct, ORMUser, ORMPrice
from src.interfaces.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import UnitOfWork
from src.infrastructure.services import ProductService
# Другие полезные методы:
# mock_method.assert_called()          # Был ли вызван хотя бы раз
# mock_method.assert_called_with(args) # Был ли вызван с конкретными аргументами (последний вызов)
# mock_method.assert_not_called()      # НЕ был вызван

# ----- # ----- # ----- Общие настройки ----- # ----- # ----- #

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

@pytest.fixture
def session():
    '''Создает временную сессию SQLite в памяти для тестов.
    Автоматически создает таблицы и закрывает сессию после использования.'''
    # Нужна ли тут какая-то модификация, rollback для транзакций??
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)  # Создаём все таблицы
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    session.begin()  # Начинаем транзакцию
    yield session
    session.rollback()  # Откатываем изменения
    session.close()

# ----- # ----- # ----- МОК ДЛЯ ПАРСЕРА # ----- # ----- # ----- #

@pytest.fixture
def mock_parser():
    parser = MagicMock()
    parser.parse_product.return_value = {
        'id': 'p1',
        'name':'Test Product',
        'image_url': 'https://example.com/image.jpg',
        'rating': 4.5,
        'categories': ['cat1', 'cat2'],
        'price_with_card': 100,
        'price_without_card': 120,
        'price_default': 150,
    }
    return parser

# ----- # ----- # ----- Product Service ----- # ----- # ----- #

@pytest.fixture
def product_service(uow):
    '''Фикстура для ProductService с реальным UnitOfWork.'''
    return ProductService(uow_factory=lambda: uow)

@pytest.fixture
def mock_product_service(mock_uow, mocker):
    uow_factory = MagicMock() # Мок для фабрики UoW
    uow_factory.return_value = mock_uow # При вызове возвращает mock_uow
    # Мокируем OzonParser
    mocker.patch('src.infrastructure.core.ozon_parser.OzonParser', return_value=MagicMock(spec=OzonParser))
    return ProductService(uow_factory=uow_factory)

# ----- # ----- # ----- MOCK UOW ----- # ----- # ----- #

@pytest.fixture(scope="function")
def mock_uow(mock_product_repo, mock_price_repo, mock_user_repo):
    '''Мок для UnitOfWork.'''
    mock_uow = MagicMock()
    mock_uow.product_repository.return_value = mock_product_repo
    mock_uow.price_repository.return_value = mock_price_repo
    mock_uow.user_repository.return_value = mock_user_repo
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    print(f"Type of mock_uow.session before assignment: {type(mock_uow.session)}")
    return mock_uow

@pytest.fixture(scope="function")
def mock_session():
    session = MagicMock(spec=Session)
    print(f"Type of session.merge in mock_session: {type(session.merge)}")
    return session

@pytest.fixture(scope="function")
def mock_product_repo(mock_session):
    repo = ProductRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_product_repo: {type(repo.session.merge)}")
    return repo

@pytest.fixture(scope="function")
def mock_price_repo(mock_session):
    repo = PriceRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_price_repo: {type(repo.session.merge)}")
    return repo

@pytest.fixture(scope="function")
def mock_user_repo(mock_session):
    repo = UserRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_user_repo: {type(repo.session.merge)}")
    return repo

# ----- # ----- # ----- Репозитории для интеграционного тестирования ----- # ----- # ----- #

@pytest.fixture
def product_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return ProductRepositoryImpl(session=session)

@pytest.fixture
def price_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return PriceRepositoryImpl(session=session)

@pytest.fixture
def user_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return UserRepositoryImpl(session=session)

@pytest.fixture
def uow():
    return UnitOfWork(session=session)

# ----- # ----- # ----- Репозитории Mock для Unit тестирования ----- # ----- # ----- #
# @pytest.fixture
# def mock_product_repo():
#     '''Мок для ProductRepository.'''
#     return MagicMock()

# @pytest.fixture
# def mock_price_repo():
#     '''Мок для PriceRepository.'''
#     return MagicMock()

# @pytest.fixture
# def mock_user_repo():
#     '''Мок для UserRepository.'''
#     return MagicMock()


# ----- # ----- # ----- Фикстуры DTO слоя ----- # ----- # ----- #

@pytest.fixture
def product_dto():
    '''Фикстура тестового Product DTO'''
    return ProductDTO(
        id='p1',
        user_id='u1',
        name='Test Product',
        link=HttpUrl('https://example.com/product'),
        image_url=HttpUrl('https://example.com/image.jpg'),
        rating=4.5,
        categories=['cat1', 'cat2']
    )

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
def user_dto():
    '''Фикстура тестового User DTO'''
    return UserDTO(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

# ----- # ----- # ----- Фикстуры DOMAIN слоя ----- # ----- # ----- #

@pytest.fixture
def product():
    '''Фикстура тестового доменного Product'''
    return Product(
        id='p1',
        user_id='u1',
        price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories=['cat1', 'cat2']
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
def user():
    '''Фикстура тестового доменного User'''
    return User(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

# ----- # ----- # ----- Фикстуры ORM слоя ----- # ----- # ----- #

@pytest.fixture
def orm_product(session):
    '''Фикстура тестового ORM Product с JSON-сериализованными категориями'''
    product = ORMProduct(
        id='p1',
        user_id='u1',
        price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories=json.dumps(['cat1', 'cat2'])  # Явная сериализация в JSON
    )
    session.add(product)
    session.commit()
    return product

@pytest.fixture
def orm_price(session):
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
    session.add(price)
    session.commit()
    return price

@pytest.fixture
def orm_user(session, orm_product):
    '''Фикстура тестового ORM User'''
    user = ORMUser(
        id='u1',
        username='test_user',
        chat_id='12345',
        #products=['p1', 'p2'] # НЕ передаем products в конструктор!
    )
    session.add(user)
    session.flush()
    user.products = [orm_product]
    session.commit()
    return user

