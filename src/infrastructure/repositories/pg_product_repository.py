from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product, PriceClaim
from src.infrastructure.database.core import with_session
from sqlalchemy import select

from src.infrastructure.database.models import ORMProduct

class PGSQLProductRepository(ProductRepository):
    @with_session
    def save_product(self, product: Product, price_claim: PriceClaim, session=None) -> None:
        '''Сохранить продукт и связанный ценовой клейм в базе данных'''
        stmt = select(ORMProduct).where(ORMProduct.product_id == product.product_id)
        result = session.execute(stmt).scalar_one_or_none()

        if result:
            # Реализовать метод для обновления товара, хотя это и должен быть save, или нет??
            pass
        if not result:
            # Что мы здесь должны вызывать то?? что то типа Product(и сюда положить данные) и еще PriceClaim()
            pass
                                                                  
        