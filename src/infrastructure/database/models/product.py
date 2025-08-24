from __future__ import annotations
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .price import ORMPrice

from .base import Base

if TYPE_CHECKING:
    from .user import ORMUser

class ORMProduct(Base):
    __tablename__ = 'products'
    
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=True)
    price_id: Mapped[str] = mapped_column(ForeignKey('prices.id'), nullable=True)

    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[str] = mapped_column(String, nullable=False)  # Храним как JSON

    # связи
    user: Mapped['ORMUser'] = relationship('ORMUser', back_populates='products', lazy='selectin')

    # история цен
    prices: Mapped[list['ORMPrice']] = relationship(
        'ORMPrice',
        back_populates='product',
        primaryjoin='ORMProduct.id == ORMPrice.product_id',
        lazy='selectin',
        cascade='all, delete-orphan'
    )
