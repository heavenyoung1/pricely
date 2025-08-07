from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .base import Base
    from .user import ORMUser

class ORMProduct(Base):
    __tablename__ = 'products'
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'))
    price_id: Mapped['ORMUser'] = mapped_column(ForeignKey('prices.id'))
    name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    categories: Mapped[str] = mapped_column(String)  # Храним как JSON
