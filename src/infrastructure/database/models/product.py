from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .base import Base
    from .user import ORMUser
    from .price_claim import ORMPriceClaim

class ORMProduct(Base):
    __tablename__ = 'products'
    product_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.user_id'))
    name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String)
    rating: Mapped[float] = mapped_column(Float)
    categories: Mapped[str] = mapped_column(String)  # Храним как JSON
    user: Mapped['ORMUser'] = relationship(back_populates='products')
    price_claims: Mapped[List['ORMPriceClaim']] = relationship(
        back_populates='product', 
        order_by='ORMPriceClaim.time_claim.desc()',
        lazy='selectin', # Улучшение производительности
        )