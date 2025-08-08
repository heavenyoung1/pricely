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
    price_id: Mapped[str] = mapped_column(ForeignKey('prices.id'))

    name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    categories: Mapped[str] = mapped_column(String)  # Храним как JSON

    # связи
    user: Mapped['ORMUser'] = relationship('ORMUser', back_populates='products')

    # текущая (последняя) цена
    price: Mapped['ORMPrice'] = relationship('ORMPrice', foreign_keys=[price_id], post_update=True)

    # история цен
    prices: Mapped[list['ORMPrice']] = relationship(
        'ORMPrice', 
        back_populates='product', 
        primaryjoin='ORMProduct.product_id == ORMPrices.product_id',  # Явно указываем условие соединения
        foreign_keys=[ORMPrice.product_id],
        )
