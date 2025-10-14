from __future__ import annotations
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .price import ORMPrice
from datetime import datetime

from . import Base

if TYPE_CHECKING:
    from .user import ORMUserProducts

class ORMProduct(Base):
    '''
    ORM модель для таблицы продуктов (products).

    Этот класс представляет таблицу продуктов в базе данных, где хранятся данные о 
    товаре, такие как артикул, название, ссылка, изображение, рейтинг, категории и цены.

    Атрибуты:
        id (str): Уникальный артикул товара (10 символов).
        name (str): Название продукта.
        link (str): Ссылка на продукт.
        image_url (str): Ссылка на изображение продукта.
        rating (float): Рейтинг продукта.
        categories (str): Категории, к которым относится продукт.
        created_at (datetime): Дата и время создания записи.
    '''
    __tablename__ = 'products'
    
    id: Mapped[str] = mapped_column(String(10), primary_key=True)  # Артикул из 10 цифр, String(10) вместо String
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    categories: Mapped[str] = mapped_column(String, nullable=False)  
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)  # Добавлен timestamp

    # Прямая связь: один продукт имеет много цен
    prices: Mapped[list['ORMPrice']] = relationship(
        'ORMPrice', 
        back_populates='product', 
        cascade='all, delete-orphan',
        )
    # Прямая связь: один продукт связан со многими пользователями через user_products
    user_products: Mapped[list['ORMUserProducts']] = relationship(
        'ORMUserProducts', 
        back_populates='product',
        cascade='all, delete-orphan',
        )