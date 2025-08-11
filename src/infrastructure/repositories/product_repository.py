import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from src.infrastructure.database.core import with_session
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class ProductRepositoryImpl(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    @with_session
    def save(self, product):
        logger.info(f'Продукт сохранен {product}')
        self.session.merge(ProductMapper.to_orm(product))

    @with_session
    def get(self, product_id):
        orm_model = self.session.get(ORMProduct, product_id)
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по id: {orm_model.id}')
        return ProductMapper.to_domain(orm_model) if orm_model else None
    
    @with_session
    def delete(self, product_id):
        orm_model = self.session.get(ORMProduct, product_id)
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по id: {orm_model.id}')
        self.session.delete(orm_model) # как дальше удалить, чтобы удалился нужный элемент

    @with_session
    def get_all(self, user_id):
        orm_model = self.session.query(ORMProduct).filter_by(user_id=user_id).all()
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по user_id: {orm_model.user_id}')
        return ProductMapper.to_domain(orm_model) if orm_model else None