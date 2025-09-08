import pytest
from src.infrastructure.services import ProductService
from src.domain.entities import User, Product, Price

@pytest.mark.integration
def test_create_and_get_user(uow, user):
    service = ProductService(uow_factory=lambda: uow)

    service.create_user(user)