from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp

from sqlalchemy.orm import Session
from infrastruture.database.core.database import engine, SessionFactory
from src.infrastruture.database.models.base import Base

from src.infrastruture.database.models.product import DBProduct
from src.infrastruture.database.models.price_stamp import DBPriceStamp
from src.infrastruture.database.models.user import DBUser


class PGSQLProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save_one_product(self, product: Product, price_stamp: PriceStamp) -> None:
        #НУЖНО ЛИ ПЕРЕДАВАТЬ СЮДА СЕССИЮ?? СЕЙЧАС ОНА НЕ ВИДНА!!!
        db_product  = DBProduct(
            id=product.id,
            user_id=product.user_id,
            name=product.name,
            rating=product.rating,
            price_with_card=product.price_with_card,
            price_without_card=product.price_without_card,
            price_default=product.price_default,
            link=product.link,
            url_image=product.url_image,
            category_product=product.category_product,
            timestamp=product.timestamp,
        )
        session.merge(db_product)

        # Сохраняем клейм цены
        db_price_stamp = DBPriceStamp(
            ID_product=product.id,
            time_stamp=price_stamp.time_stamp,
            price_with_card=price_stamp.price_with_card,
            price_without_card=price_stamp.price_without_card,
            previous_price_without_card=price_stamp.previous_price_without_card,
            price_default=price_stamp.price_default,
        )
        session.add(db_price_stamp)
        session.commit()

    def save_few_products(self, products: List[Product], price_stamp: PriceStamp) -> None:
        for product in products:
            self.save_one_product(product)

    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        
            
            
