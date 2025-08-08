from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct


class ORMUser(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(String, primary_key=True)

    username: Mapped[str] = mapped_column(String)
    chat_id: Mapped[str] = mapped_column(String)

    products: Mapped[list['ORMProduct']] = relationship('ORMProduct', back_populates='user')
