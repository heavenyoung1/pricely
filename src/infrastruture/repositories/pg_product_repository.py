from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp

from sqlalchemy.orm import Session
from infrastruture.database.core.database import engine, SessionFactory
from src.infrastruture.database.models.base import Base


class PGSQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

