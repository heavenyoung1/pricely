import pytest
import json
from src.application.use_cases.create_product import CreateProductUseCase, ProductCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_product_create_success(
        session,
        product_repo, 
        price_repo, 
        user_repo, 
        product,
        price,
        user,
        ):
    # Добавляем пользователя в базу, чтобы пройти проверку existing_user
    session.add(ORMUser(id=user.id, username=user.username, chat_id=user.chat_id, products=[]))
    session.commit()

    assert product_repo.get(product.id) is None
