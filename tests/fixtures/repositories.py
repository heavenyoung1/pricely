import pytest
from unittest.mock import Mock, MagicMock
from src.application.interfaces.repositories import (
    ProductRepository,
    PriceRepository,
    UserRepository,
    UserProductsRepository,
)

from src.infrastructure.database.repositories import (
    ProductRepositoryImpl,
    PriceRepositoryImpl,
    UserRepositoryImpl,
    UserProductsRepositoryImpl,
)

import logging

logger = logging.getLogger(__name__)

# ----- РЕПОЗИТОРИИ ДЛЯ ИНТЕГРАЦИОННЫХ - ТЕСТОВ С DB-SESSION -----  #


@pytest.fixture
def product_repo(db_session):  # ← Использует реальную сессию PostgreSQL
    """Фикстура репозитория продуктов с сессией."""
    return ProductRepositoryImpl(session=db_session)


@pytest.fixture
def price_repo(db_session):  # ← Использует реальную сессию с PostgreSQL
    """Фикстура репозитория продуктов с сессией."""
    return PriceRepositoryImpl(session=db_session)


@pytest.fixture
def user_repo(db_session):  # ← Использует реальную сессию с PostgreSQL
    """Фикстура репозитория продуктов с сессией."""
    return UserRepositoryImpl(session=db_session)


@pytest.fixture
def user_product_repo(db_session):  # ← Использует реальную сессию с PostgreSQL
    """Фикстура репозитория свзяи пользователей и товаров (M2M) с сессией."""
    return UserProductsRepositoryImpl(session=db_session)


# ----- ЗАМОКАНЫЕ РЕПОЗИТОРИИ ДЛЯ UNIT - ТЕСТОВ -----  #


@pytest.fixture
def mock_product_repo(mock_session):  # ← Использует мокированную сессию
    """Фикстура репозитория товаров с замоканной сессией."""
    logger.debug(f"TYPE OF MOCK PRODUCT REPO {type(mock_product_repo)}")
    return ProductRepositoryImpl(session=mock_session)


@pytest.fixture
def mock_price_repo(mock_session):  # ← Использует мокированную сессию
    """Фикстура репозитория товаров с замоканной сессией."""
    return PriceRepositoryImpl(session=mock_session)


@pytest.fixture
def mock_user_repo(mock_session):  # ← Использует мокированную сессию
    """Фикстура репозитория свзяи пользователей и товаров (M2M) с замоканной сессией."""
    return UserRepositoryImpl(session=mock_session)


@pytest.fixture
def mock_user_products_repo(mock_session):  # ← Использует мокированную сессию
    """Фикстура репозитория товаров с замоканной сессией."""
    return UserProductsRepositoryImpl(session=mock_session)


# ----- PURE MOCK РЕПОЗИТОРИИ ДЛЯ UNIT - ТЕСТОВ ЗАВЯЗАННЫЕ НА ИНТЕРФЕЙС -----  #


@pytest.fixture
def pure_mock_product_repo():
    """Чистый мок ProductRepository для unit-тестов UseCase."""
    mock = Mock(spec=ProductRepository)  # Используем интерфейс
    mock.get.return_value = None  # По умолчанию товар не найден
    mock.save.return_value = None
    return mock


@pytest.fixture
def pure_mock_price_repo():
    """Чистый мок PriceRepository для unit-тестов UseCase."""
    mock = Mock(spec=PriceRepository)  # Используйте интерфейс
    mock.save.return_value = None
    return mock


@pytest.fixture
def pure_mock_user_repo():
    """Чистый мок UserRepository для unit-тестов UseCase."""
    mock = Mock(spec=UserRepository)  # Используйте интерфейс
    mock.get.return_value = None  # По умолчанию пользователь не найден
    mock.save.return_value = None
    return mock


@pytest.fixture
def pure_mock_user_products_repo():
    """Чистый мок UserProductsRepositoryImpl для unit-тестов UseCase."""
    mock = Mock(spec=UserProductsRepositoryImpl)  # Используйте интерфейс
    # mock.get.return_value = None  # По умолчанию пользователь не найден
    # mock.save.return_value = None
    return mock
