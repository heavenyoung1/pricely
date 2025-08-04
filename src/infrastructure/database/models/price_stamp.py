from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.product import DBProduct


if TYPE_CHECKING:
    from src.domain.entities.price import PriceStamp


class DBPriceStamp(Base):
    '''Модель клейма цены для БД
    
    Attributes:
        ID_stamp: Уникальный идентификатор клейма
        ID_product: ID продукта
        time_stamp: Временная метка
        price_with_card: Цена с картой
        price_without_card: Цена без карты
        previous_price_with_card: Предыдущая цена с картой
        previous_price_without_card: Предыдущая цена без карты
        price_default: Цена по умолчанию
        '''
    __tablename__ = 'price_stamps'

    ID_stamp: Mapped[str] = mapped_column(primary_key=True)
    ID_product: Mapped[str] = mapped_column(String, ForeignKey('products.product_id'), index=True)
    time_stamp: Mapped[datetime] = mapped_column(DateTime())
    price_with_card: Mapped[int] = mapped_column(Integer())
    price_without_card: Mapped[int] = mapped_column(Integer())
    previous_price_with_card: Mapped[int] = mapped_column(Integer())
    previous_price_without_card: Mapped[int] = mapped_column(Integer())
    price_default: Mapped[int] = mapped_column(Integer())

    # Relationships
    product: Mapped['DBProduct'] = relationship(back_populates='price_stamps')

    def to_domain(self) -> 'PriceStamp':
        from src.domain.entities.price import PriceStamp
        return PriceStamp(
            ID_stamp=self.ID_stamp,
            ID_product=self.ID_product,
            time_stamp=self.time_stamp,
            price_with_card=self.previous_price_with_card,
            price_without_card=self.price_without_card,
            previous_price_with_card=self.previous_price_with_card,
            previous_price_without_card=self.previous_price_without_card,
            price_default=self.price_default,
        )