from __future__ import annotations
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from .price import ORMPrice
from datetime import datetime

# ТУт нужно доделать свящи с другими таблицами
from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct, ORMUser

class ORMUserProducts(Base):
    __tablename__ = 'users_products'
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    product_id: Mapped[str] = mapped_column(String, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)

    # Обратные связи: запись user_products принадлежит пользователю и продукту
    user: Mapped["ORMUser"] = relationship("ORMUser", back_populates="user_products")
    product: Mapped["ORMProduct"] = relationship("ORMProduct", back_populates="user_products")