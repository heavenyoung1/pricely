from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct


class ORMPrice(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)  # Автоинкремент для id
    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True
    )  # Связь с продуктом, при удалении продукта цены тоже удаляются

    with_card: Mapped[int] = mapped_column(Integer, nullable=False)
    without_card: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_with_card: Mapped[int] = mapped_column(Integer, nullable=True)
    previous_without_card: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # Обратная связь: цены принадлежат одному продукту
    product: Mapped["ORMProduct"] = relationship("ORMProduct", back_populates="prices")
