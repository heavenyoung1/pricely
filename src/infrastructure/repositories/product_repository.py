from src.domain.repositories import ProductRepository
from src.domain.entities import Product
from src.infrastructure.mappers.product_mapper import ProductMapper
from src.infrastructure.database.models import ORMProduct
from src.infrastructure.database.core.database import with_session
from sqlalchemy.orm import Session
from typing import List

class SqlAlchemyProductRepository(ProductRepository):

    @with_session
    def save(self, product: Product, session: Session) -> None:
        orm_product = ProductMapper.to_orm(product)
        session.merge(orm_product)

    @with_session
    def get_product(self, product: Product, session: Session) -> Product:
        orm_product = session.get(ORMProduct,product.id)
        return ProductMapper.to_entity(orm_product) if orm_product else None
    
    @with_session
    def delete_product(self, product_id, session: Session) -> None:
        product = session.get(ORMProduct, product_id)
        if product:
            session.delete(product)

    @with_session
    def get_all_product(self, user_id, session: Session) -> list['Product']:
        # А вот оно точно будет работать??))
        products = session.query(ORMProduct).filter_by(user_id=user_id).all() 
        return [ProductMapper.to_entity(product) for product in products]