import pytest
import logging
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import MagicMock
from pydantic import HttpUrl

from src.infrastructure.database.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.models import Base, ORMProduct, ORMUser, ORMPrice
from src.application.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User
from src.core.uow import SQLAlchemyUnitOfWork
from src.infrastructure.parsers import OzonParser
from src.infrastructure.services import ProductService

pytest_plugins = [
    'fixtures.database',
    'fixtures.product',
    'fixtures.price', 
    'fixtures.user',
    'fixtures.repositories',
    'fixtures.service',
]

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


