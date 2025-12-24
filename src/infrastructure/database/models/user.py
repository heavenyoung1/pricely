from __future__ import annotations
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from . import ORMUserProducts


class ORMUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True
    )  # Уникальный идентификатор пользователя
    username: Mapped[str] = mapped_column(String, nullable=False)  # Имя пользователя
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )  # Дата создания

    # Прямая связь: один пользователь связан со многими записями user_products
    user_products: Mapped[list["ORMUserProducts"]] = relationship(
        "ORMUserProducts",
        back_populates="user",
    )
