from __future__ import annotations
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from .price import ORMPrice
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct
    from .user import ORMUser


class ORMUserProducts(Base):
    """
    ORM модель для таблицы связи между пользователями и продуктами (users_products).

    Этот класс представляет таблицу, которая связывает пользователей и продукты. Каждый пользователь
    может быть связан с несколькими продуктами, и каждый продукт может быть связан с несколькими пользователями.

    Атрибуты:
        user_id (str): Идентификатор пользователя.
        product_id (str): Идентификатор продукта.
    """

    __tablename__ = "users_products"

    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )  # Идентификатор пользователя, внешний ключ

    product_id: Mapped[str] = mapped_column(
        String, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    )  # Идентификатор продукта, внешний ключ

    # Обратные связи: запись user_products принадлежит пользователю и продукту
    user: Mapped["ORMUser"] = relationship("ORMUser", back_populates="user_products")
    product: Mapped["ORMProduct"] = relationship(
        "ORMProduct", back_populates="user_products"
    )
