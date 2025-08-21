import pytest
import json
from src.application.use_cases.create_product import CreateProductUseCase, ProductCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
    