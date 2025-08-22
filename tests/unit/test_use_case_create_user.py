import pytest
import json
from src.application.use_cases.create_user import CreateUserUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_create_user_use_case_success(
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
    ):

    # Настраиваем моки
    mock_user_repo.get.return_value = None      # Пользователь НЕ существует