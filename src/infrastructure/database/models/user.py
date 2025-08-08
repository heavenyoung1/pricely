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

    username: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[str] = mapped_column(String, nullable=False)

    products: Mapped[list['ORMProduct']] = relationship(
        'ORMProduct',
        back_populates='user',
        lazy='selectin',
        cascade='all, delete-orphan'
    )

    # lazy='selectin' для эффективной загрузки
    # cascade='all, delete-orphan' для удаления связанных продуктов при удалении пользователя
