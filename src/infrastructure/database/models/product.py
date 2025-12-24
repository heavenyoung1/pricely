from __future__ import annotations
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .price import ORMPrice
from datetime import datetime

from . import Base

if TYPE_CHECKING:
    from .user import ORMUserProducts


class ORMProduct(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )  # Добавлен timestamp

    # Прямая связь: один продукт имеет много цен
    prices: Mapped[list["ORMPrice"]] = relationship(
        "ORMPrice",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    # Прямая связь: один продукт связан со многими пользователями через user_products
    user_products: Mapped[list["ORMUserProducts"]] = relationship(
        "ORMUserProducts",
        back_populates="product",
        cascade="all, delete-orphan",
    )
