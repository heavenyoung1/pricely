import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.application.interfaces.repositories import PriceRepository
from src.infrastructure.database.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice, ORMProduct

logger = logging.getLogger(__name__)


class PriceRepositoryImpl(PriceRepository):
    '''Реализация репозитория для работы с ценами в базе данных.'''
    def __init__(self, session: Session):
        self.session = session

    def save(self, price: Price) -> None:
        try:
            logger.info(f"Сохранение цены: {price}")
            orm_price = PriceMapper.domain_to_orm(price)
            self.session.merge(orm_price) # НУЖНА, НО ПОЧЕММУ???
            logger.debug(f"Цена успешно сохранена (ID: {orm_price.id})")
        except Exception as e:
            logger.error(f"Ошибка сохранения цены {price}: {str(e)}")
            raise
    
    def get(self, price_id: str) -> Optional[Price]:
        logger.debug(f"Поиск цены по ID: {price_id}")
        orm_model = self.session.get(ORMPrice, price_id)
        if not orm_model:
            logger.warning(f"Цена с ID {price_id} не найдена")
            return None
        price = PriceMapper.orm_to_domain(orm_model)
        logger.info(f"Найдена цена: {price} (ID: {orm_model.id})")
        return price
    
    def get_all_prices_by_product(self, product_id: str) -> List[Price]:
        logger.debug(f"Получение всех цен для продукта {product_id}")
        try:
            orm_prices = self.session.query(ORMPrice).filter_by(product_id=product_id).all()
            prices = [PriceMapper.orm_to_domain(p) for p in orm_prices]
            logger.info(f"Найдено {len(prices)} цен для продукта {product_id}")
            return prices
        except Exception as e:
            logger.error(f"Ошибка получения цен для продукта {product_id}: {str(e)}")
            raise
    
    def delete(self, price_id: str) -> bool:
        logger.info(f"Попытка удаления цены с ID: {price_id}")
        orm_price = self.session.get(ORMPrice, price_id)
        if not orm_price:
            logger.warning(f"Цена с ID {price_id} не найдена для удаления")
            return False
        try:
            self.session.delete(orm_price)
            #self.session.commit() ТРАНЗАКЦИЯМИ УПРАВЛЯЕМ В UOW!!! 
            logger.info(f"Цена с ID {price_id} успешно удалена")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления цены {price_id}: {str(e)}")
            raise

    def get_latest_for_product(self, product_id: str) -> Price | None:
        ''''''
        logger.debug(f'Получение последней цены для продукта {product_id}')
        orm_price = (
            self.session.query(ORMPrice).filter(ORMPrice.product_id == product_id).order_by(desc(ORMPrice.created_at)).first()
        )
        if not orm_price:
            logger.info(f'Для продукта {product_id} нет данных о цене')
            return None
        
        return Price(
            id=orm_price.id,
            product_id=orm_price.product_id,
            with_card=orm_price.with_card,
            without_card=orm_price.without_card,
            previous_with_card=orm_price.previous_with_card,
            previous_without_card=orm_price.previous_without_card,
            created_at=orm_price.created_at,
        )