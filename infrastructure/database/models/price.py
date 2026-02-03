from sqlalchemy import String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from infrastructure.database.models.base import Base


class ORMPrice(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True
    )

    with_card: Mapped[int] = mapped_column(Integer, nullable=False)
    without_card: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_with_card: Mapped[int] = mapped_column(Integer, nullable=True)
    previous_without_card: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    product: Mapped['ORMProduct'] = relationship('ORMProduct', back_populates='prices')
