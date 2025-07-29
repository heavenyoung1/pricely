from src.infrastruture.database.base import Base

from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class DBUser(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    product_id: Mapped[str] = mapped_column(String, ForeignKey('product.product_id'), index=True)