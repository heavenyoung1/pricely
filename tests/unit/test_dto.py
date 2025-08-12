import pytest
from datetime import datetime
from pydantic import HttpUrl

from interfaces.dto.dto_to_domain import ProductCreateDTO, PriceCreateDTO, UserCreateDTO
from interfaces.dto.dto_to_domain import product_dto_to_entity, price_dto_to_entity, user_dto_to_entity
from src.domain.entities import Product, Price, User