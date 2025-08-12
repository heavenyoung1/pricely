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

