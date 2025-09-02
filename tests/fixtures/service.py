import pytest

from src.core.uow import SQLAlchemyUnitOfWork
from src.infrastructure.services import ProductService

@pytest.fixture
def product_service(session_factory):
    return ProductService(
        lambda: SQLAlchemyUnitOfWork(session_factory=session_factory)
        )