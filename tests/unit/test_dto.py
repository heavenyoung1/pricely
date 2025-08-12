import pytest
from datetime import datetime
from pydantic import HttpUrl

from src.interfaces.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User

# ----- # ----- # ----- ТОВАР ----- # ----- # ----- #

def test_product_DTO_domain(product_dto):
    domain = product_dto.to_domain()
    assert isinstance(domain, Product)
    assert product_dto.id == domain.id
    assert product_dto.name == domain.name

def test_price_DTO_domain(price_dto):
    domain = price_dto.to_domain()
    assert isinstance(domain, Price)
    assert price_dto.id == domain.id
    assert price_dto.product_id == domain.product_id

def test_user_DTO_domain(user_dto):
    domain = user_dto.to_domain()
    assert isinstance(domain, User)
    assert user_dto.id == domain.id
    assert user_dto.username == domain.username

