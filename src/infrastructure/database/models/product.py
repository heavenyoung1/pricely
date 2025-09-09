from __future__ import annotations
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional
from .price import ORMPrice

from .base import Base

if TYPE_CHECKING:
    from .user import ORMUser

class ORMProduct(Base):
    __tablename__ = 'products'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    # 👇 ключевой момент: nullable + SET NULL, чтобы разорвать цикл при дропе и вставке
    price_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("prices.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[str] = mapped_column(String, nullable=False)  # Храним как JSON

    # связь с пользователем
    user: Mapped['ORMUser'] = relationship(
        'ORMUser',
        back_populates='products',
        lazy='selectin'
    )

    # связь с актуальной ценой
    current_price: Mapped['ORMPrice'] = relationship(
        'ORMPrice',
        foreign_keys=[price_id],
        post_update=True,  # фиксируем цикл product <-> price
        lazy='selectin',
        uselist=False
    )

    # все цены по продукту
    prices: Mapped[list['ORMPrice']] = relationship(
        'ORMPrice',
        back_populates='product',
        foreign_keys='ORMPrice.product_id',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
