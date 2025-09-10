from __future__ import annotations
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from .price import ORMPrice
from datetime import datetime


from .base import Base

class ORMUserProducts(Base):
    __tablename__ = 'users_products'
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)