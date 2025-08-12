import pytest
from datetime import datetime
from pydantic import HttpUrl

from src.interfaces.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User

def test_product_DTO_entity():
    dt- = ProductDTO