from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

from infrastructure.database.models.base import Base
from infrastructure.database.models.price import ORMPrice
from infrastructure.database.models.user_products import ORMUserProducts


class ORMProduct(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    articule: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    change: Mapped[int] = mapped_column(Integer, default=5)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    prices: Mapped[List['ORMPrice']] = relationship(
        'ORMPrice', back_populates='product', cascade='all, delete-orphan'
    )
    user_products: Mapped[List['ORMUserProducts']] = relationship(
        'ORMUserProducts', back_populates='product', cascade='all, delete-orphan'
    )
