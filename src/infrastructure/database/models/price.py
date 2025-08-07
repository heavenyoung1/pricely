from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from . import ORMProduct

class ORMPrice(Base):
    __tablename__ = 'prices'
    id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped['ORMProduct'] = mapped_column(ForeignKey('products.id'))
    with_card: Mapped[int] = mapped_column(Integer)
    without_card: Mapped[int] = mapped_column(Integer)
    previous_with_card: Mapped[int] = mapped_column(Integer)
    previous_without_card: Mapped[int] = mapped_column(Integer)
    default: Mapped[int] = mapped_column(Integer)
    date_claim: Mapped[datetime] = mapped_column(DateTime)