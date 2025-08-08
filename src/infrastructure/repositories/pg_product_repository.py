from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product, Price
from src.infrastructure.database.core import with_session

from src.infrastructure.mappers import ProductMapper, PriceMapper
from sqlalchemy import select

from src.infrastructure.database.models import ORMProduct, ORMPrice

class PGSQLProductRepository(ProductRepository):
    @with_session
    def save_product(self, product: Product, price: Price , session: Session = None) -> None:
        '''Сохранить продукт и связанную с ним цену'''
        
        # Проверяем, существует ли товар
        stmt = select(ORMProduct).where(ORMProduct.id == product.id)
        existing_product = session.execute(stmt).scalar_one_or_none()     

        # Проверяем, существует ли цена
        stmt = select(ORMPrice).where(ORMPrice.id == price.id)
        existing_price = session.execute(stmt).scalar_one_or_none()




