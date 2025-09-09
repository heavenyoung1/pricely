import pytest
from src.infrastructure.services import ProductService
from src.domain.entities import User, Product, Price

@pytest.mark.integration
def test_create_and_get_user(uow, user, mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=mock_parser)

    service.create_user(user)