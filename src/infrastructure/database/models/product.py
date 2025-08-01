from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

from src.infrastructure.database.models.base import Base

if TYPE_CHECKING:
    from .user import DBUser
    from .price_stamp import DBPriceStamp

class DBProduct(Base):
    '''Модель продукта для БД
    
    Attributes:
        product_id: Уникальный идентификатор товара
        user_id: ID пользователя, которому принадлежит товара
        name: Название товара
        link: Ссылка на товара
        url_image: Ссылка на изображение товара
        rating: Рейтинг товара
        price_with_card: Цена
        price_without_card: Цена без карты
        previous_price_with_card: Предыдущая цена с картой
        previous_price_without_card: Предыдущая цена без карты
        price_default: Цена по умолчанию (без скидок и прочего)
        category_product: Категории продукта
        last_timestamp: Время последнего клейма
        user: Ссылка на пользователя (отношение многие-к-одному)
        price_stamps: История цен продукта (отношение один-ко-многим)
        '''
    __tablename__ = 'products' 

    # string data type
    product_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey('users.id'), index=True)
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
    last_timestamp: Mapped[datetime] = mapped_column(DateTime())
    
    # relationships
    user: Mapped['DBUser'] = relationship('DBUser', back_populates='products')
    price_stamps: Mapped[List['DBPriceStamp']] = relationship(
        back_populates='product',
        cascade="all, delete-orphan"
    ) # Каскадное удаление

    last_stamp: Mapped['DBPriceStamp'] = relationship(
        foreign_keys='[DBPriceStamp.ID_product]',
        primaryjoin='and_(DBProduct.product_id == DBPriceStamp.ID_product, '
                'DBPriceStamp.time_stamp == DBProduct.last_timestamp)',
        viewonly=True,
        uselist=False
    )
