from __future__ import annotations
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from . import ORMUserProducts


class ORMUser(Base):
    """
    ORM модель для таблицы пользователей (users).

    Этот класс представляет таблицу пользователей в базе данных, где хранятся данные о пользователе,
    такие как уникальный идентификатор, имя пользователя, идентификатор чата и дата создания.

    Атрибуты:
        id (str): Уникальный идентификатор пользователя.
        username (str): Имя пользователя.
        chat_id (str): Идентификатор чата пользователя (например, в Telegram).
        created_at (datetime): Дата и время создания пользователя.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, primary_key=True
    )  # Уникальный идентификатор пользователя
    username: Mapped[str] = mapped_column(String, nullable=False)  # Имя пользователя
    chat_id: Mapped[str] = mapped_column(String, nullable=False)  # Идентификатор чата
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )  # Дата создания

    # Прямая связь: один пользователь связан со многими записями user_products
    user_products: Mapped[list["ORMUserProducts"]] = relationship(
        "ORMUserProducts",
        back_populates="user",
    )
