from sqlalchemy import String
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct


class ORMUser(Base):
    __tablename__ = 'users'
    user_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String)
    chat_id: Mapped[str] = mapped_column(String)
    products: Mapped[List['ORMProduct']] = mapped_column(ForeignKey('products.user_id'))