from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct

class ORMPrice(Base):
    __tablename__ = 'prices'

    id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.id'), nullable=False)

    with_card: Mapped[int] = mapped_column(Integer, nullable=False)
    without_card: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_with_card: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_without_card: Mapped[int] = mapped_column(Integer, nullable=False)
    default: Mapped[int] = mapped_column(Integer, nullable=False)

    date_claim: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # связь с товаром
    product: Mapped['ORMProduct'] = relationship(
        'ORMProduct',
        back_populates='prices',
        foreign_keys=[product_id],
        lazy='selectin'
    )