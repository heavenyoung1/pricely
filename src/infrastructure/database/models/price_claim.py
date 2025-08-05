from datetime import datetime
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .base import Base
    from .price import ORMPrice
    from .product import ORMProduct

class ORMPriceClaim(Base):
    __tablename__ = 'price_claims'
    claim_id: Mapped[str] = mapped_column(primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey('products.product_id'), index=True)
    time_claim: Mapped[datetime] = mapped_column(DateTime, index=True)
    price: Mapped['ORMPrice'] = relationship(back_populates='price_claim')
    product: Mapped['ORMProduct'] = relationship(back_populates='price_claims')