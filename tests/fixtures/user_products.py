import pytest
from src.infrastructure.database.models import ORMUserProducts


@pytest.fixture
def orm_user_products(orm_user):
    mock_product = ORMUserProducts(user_id=orm_user.id, product_id="p1")
    return [mock_product]
