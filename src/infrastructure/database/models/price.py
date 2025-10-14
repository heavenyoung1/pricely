from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import ORMProduct

class ORMPrice(Base):
    '''
    ORM модель для таблицы цен (prices).

    Этот класс представляет таблицу цен в базе данных, где хранятся данные о ценах 
    товаров с картой и без карты, а также связь с продуктом.

    Атрибуты:
        id (int): Уникальный идентификатор записи (автоинкремент).
        product_id (str): Идентификатор продукта, к которому привязана цена.
        with_card (int): Цена с картой.
        without_card (int): Цена без карты.
        previous_with_card (Optional[int]): Предыдущая цена с картой.
        previous_without_card (Optional[int]): Предыдущая цена без карты.
        created_at (datetime): Дата создания записи.
    '''
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Автоинкремент для id
    product_id: Mapped[str] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )  # Связь с продуктом, при удалении продукта цены тоже удаляются

    with_card: Mapped[int] = mapped_column(Integer, nullable=False)
    without_card: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_with_card: Mapped[int] = mapped_column(Integer, nullable=True)
    previous_without_card: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    # Обратная связь: цены принадлежат одному продукту
    product: Mapped["ORMProduct"] = relationship("ORMProduct", back_populates="prices")