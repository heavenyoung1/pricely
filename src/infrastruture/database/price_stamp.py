from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.infrastruture.database.base import Base


class DBPriceStamp(Base):
    '''Модель клейма цены для БД'''
    __tablename__ == 'price_stamps'

    ID_stamp: Mapped[str] = mapped_column(primary_key=True)
    ID_product: Mapped[str] = mapped_column(String, ForeignKey("product.id"), index=True)
    time_stamp: Mapped[datetime] = mapped_column(DateTime())
    price_with_card: Mapped[int] = mapped_column(Integer())
    price_without_card: Mapped[int] = mapped_column(Integer())
    previous_price_with_card: Mapped[int] = mapped_column(Integer())
    previous_price_without_card: Mapped[int] = mapped_column(Integer())
    price_default: Mapped[int] = mapped_column(Integer())