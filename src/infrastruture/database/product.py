from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class DBProduct(Base):
    __tablename__ = 'products'

    # string data type
    product_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    link: Mapped[str] = mapped_column(String(500)) 
    url_image: Mapped[str] = mapped_column(String(500))

    # numeric data type
    rating: Mapped[float] 
    price_with_card: Mapped[int] 
    price_without_card: Mapped[int] 
    previous_price_with_card: Mapped[int] 
    previous_price_without_card: Mapped[int] 
    price_default: Mapped[int] 
    #discount_amount: Mapped[float] 

    # special data type
    category_product: Mapped[List[str]]
    last_timestamp: Mapped[datetime]
