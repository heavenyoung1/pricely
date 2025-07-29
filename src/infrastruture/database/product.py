from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, JSON
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
    rating: Mapped[float]  = mapped_column(Float(precision=2))  # 2 знака после запятой
    price_with_card: Mapped[int] = mapped_column(Integer())
    price_without_card: Mapped[int] = mapped_column(Integer())
    previous_price_with_card: Mapped[int] = mapped_column(Integer())
    previous_price_without_card: Mapped[int] = mapped_column(Integer())
    price_default: Mapped[int] = mapped_column(Integer())
    #discount_amount: Mapped[float] 

    # special data type
    
    category_product: Mapped[List[str]] = mapped_column(JSON)  # Для хранения списка
    ID_last_stamp: Mapped[str] = mapped_column(String, ForeignKey("price_stamps.ID_stamp"), index=True)
    last_timestamp: Mapped[datetime] = mapped_column(DateTime())
