from __future__ import annotations
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime
from . import ORMUserProducts

from .base import Base


class ORMUser(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    chat_id: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    # Прямая связь: один пользователь связан со многими записями user_products
    user_products: Mapped[list["ORMUserProducts"]] = relationship("ORMUserProducts", back_populates="user")