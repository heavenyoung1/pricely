from sqlalchemy.orm import Session
from src.interfaces.repositories import ProductRepository
from src.domain.entities import Product
from src.infrastructure.database.core import with_session

from src.infrastructure.mappers import ProductMapper
from sqlalchemy import select

from src.infrastructure.database.models import ORMProduct

class PGSQLProductRepository(ProductRepository):
    @with_session
    def save_product(self, product: Product, session: Session = None) -> None:
        '''Сохранить продукт и связанный ценовой клейм в базе данных'''
        
        # Проверяем, существует ли продукт
        stmt = select(ORMProduct).where(ORMProduct.product_id == product.product_id)
        existing_product = session.execute(stmt).scalar_one_or_none()       
        