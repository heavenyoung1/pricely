import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class ProductRepositoryImpl(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, product):
        logger.info(f'Продукт сохранен {product}')
        self.session.merge(ProductMapper.to_orm(product))

    def get(self, product_id):
        orm_model = self.session.get(ORMProduct, product_id)
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по id: {orm_model.id}')
        return ProductMapper.to_domain(orm_model) if orm_model else None
    
    def delete(self, product_id):
        orm_model = self.session.get(ORMProduct, product_id)
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по id: {orm_model.id}')
        self.session.delete(orm_model) # как дальше удалить, чтобы удалился нужный элемент

    def get_all(self, user_id):
        orm_model = self.session.get(ORMProduct, user_id)
        logger.info(f'Продукт {ProductMapper.to_domain(orm_model)} получен по user_id: {orm_model.user_id}')
        return ProductMapper.to_domain(orm_model) if orm_model else None