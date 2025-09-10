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
    
    id: Mapped[str] = mapped_column(String,primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[str] = mapped_column(String, nullable=False)