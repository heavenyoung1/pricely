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
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    price_id: Mapped[str] = mapped_column(ForeignKey('prices.id'), nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[str] = mapped_column(String, nullable=False)  # Храним как JSON

    user: Mapped['ORMUser'] = relationship('ORMUser', back_populates='products', lazy='selectin')

    # СВЯЗЬ С ТЕКУЩЕЙ ЦЕНОЙ (через price_id)
    current_price: Mapped['ORMPrice'] = relationship(
        'ORMPrice',
        foreign_keys=[price_id],
        post_update=True,  # Избегаем циклических ссылок при обновлении
        lazy='selectin'
    )

    # СВЯЗЬ СО ВСЕМИ ЦЕНАМИ (история цен через Price.product_id)
    prices: Mapped[list['ORMPrice']] = relationship(
        'ORMPrice',
        back_populates='product',
        foreign_keys='ORMPrice.product_id',  # Явно указываем FK
        cascade='all, delete-orphan',
        lazy='selectin'
    )
