import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class PriceRepositoryImpl(PriceRepository):
    def __init__(self, session: Session, product_repository: ProductRepository):
        self.session = session
        self.product_repository = product_repository

    def save(self, price):
        self.session.merge(PriceMapper.to_orm(price))

    def get_relevant_price_id(self, product_id):
        # Здесь мы получаем актуальную цену по USER_ID??
        # Ведь нелогично получать просто цену
        # Мы должны получать МОДЕЛЬ PRICE в зависимости от того какой PRICE_ID в модели PRODUCT!!!
        orm_model = self.session.get(ORMProduct, product_id)
        domain_model = ProductMapper.to_domain(orm_model)
        logger.info(f'Продукт {domain_model} получен по id: {domain_model.id}')
        price_id = domain_model.price_id
        return PriceMapper.to_domain(price_id) if price_id else None
    
    def get(self, product_id):
        price_id = self.product_repository._get_relevant_price_id(product_id)
        orm_price = self.session.get(ORMPrice, price_id)
        return PriceMapper.to_domain(orm_price) if orm_price else None
    
    def delete(self, product_id):
        orm_price = self.session.get(ORMPrice, product_id)
        self.session.delete(ORMPrice, orm_price) # Так ли это, правильно ли написано??

    def get_all(self, user_id):
        orm_prices = self.session.get(ORMPrice, user_id)
        # Их тут должно быть несколько, как их отображать??
        for orm_price in orm_price:
            logger.info(f'{orm_price}')
        # Чекнуть вывод и переписать функцию!!!


