from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.product import ORMProduct
from src.infrastructure.database.models.user import ORMUser


class ORMUserProducts(Base):
    __tablename__ = 'user_products'

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )  # Идентификатор пользователя, внешний ключ

    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('products.id', ondelete='CASCADE'), primary_key=True
    )  # Идентификатор продукта, внешний ключ

    # Relationships
    user: Mapped['ORMUser'] = relationship('ORMUser', back_populates='user_products')
    product: Mapped['ORMProduct'] = relationship(
        'ORMProduct', back_populates='user_products'
    )
