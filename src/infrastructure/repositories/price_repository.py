import logging
from sqlalchemy.orm import Session
from typing import Optional, List , TYPE_CHECKING    

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from src.infrastructure.database.core import with_session

if TYPE_CHECKING:
    from src.domain.entities import Product, Price

logger = logging.getLogger(__name__)

class PriceRepositoryImpl(PriceRepository):
    def __init__(self, session: Session, product_repository: ProductRepository):
        self.session = session
        self.product_repository = product_repository

    @with_session
    def save(self, price: Price, session: Session) -> None:
        orm_price = PriceMapper.to_orm(price)
        session.merge(orm_price)
        logger.info(f'Цена сохранена: {price}')

    @with_session
    def get_relevant_price_id(self, product_id: str, session: Session) -> Optional[str]:
        orm_product = session.get(ORMProduct, product_id)
        if orm_product:
            price_id = orm_product.price_id  # Предполагаю, что в ORMProduct есть поле price_id
            logger.info(f'Актуальный price_id для продукта {product_id}: {price_id}')
            return price_id
        logger.warning(f'Продукт с id {product_id} не найден')
        return None
    
    @with_session
    def get(self, price_id: str, session: Session) -> Optional[Price]:
        orm_price = session.get(ORMPrice, price_id)
        if orm_price:
            price = PriceMapper.to_domain(orm_price)
            logger.info(f'Цена {price} получена по id: {price_id}')
            return price
        logger.warning(f'Цена с id {price_id} не найдена')
        return None
    
    @with_session
    def get_prices_by_product(self, product_id: str, session: Session) -> List[Price]:
        orm_prices = session.query(ORMPrice).filter(ORMPrice.product_id == product_id).all()
        prices = [PriceMapper.to_domain(orm_price) for orm_price in orm_prices]
        logger.info(f'Получено {len(prices)} цен для продукта {product_id}')
        return prices
    
    @with_session
    def get_all(self, user_id: str, session: Session) -> List[Price]:
        orm_prices = session.query(ORMPrice).filter(ORMPrice.user_id == user_id).all()
        prices = [PriceMapper.to_domain(orm_price) for orm_price in orm_prices]
        logger.info(f'Получено {len(prices)} цен для пользователя {user_id}')
        return prices
    
    @with_session
    def delete(self, price_id: str, session: Session) -> None:
        orm_price = session.get(ORMPrice, price_id)
        if orm_price:
            session.delete(orm_price)
            logger.info(f'Цена удалена по id: {price_id}')
        else:
            logger.warning(f'Цена с id {price_id} не найдена')




