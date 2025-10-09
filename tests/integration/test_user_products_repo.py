import pytest

from src.infrastructure.database.models import ORMUserProducts
from src.infrastructure.database.repositories import UserProductsRepositoryImpl

import logging
logger = logging.getLogger(__name__)


# @pytest.mark.integration
# def test_get_success_data(mock_session):
#     repo = UserProductsRepositoryImpl(session=mock_session)
#     repo.get_all_user_products_pair()