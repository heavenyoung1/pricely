import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.repositories import PriceRepository
from src.infrastructure.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice, ORMProduct

logger = logging.getLogger(__name__)


class PriceRepositoryImpl(PriceRepository):
    '''Реализация репозитория для работы с ценами в базе данных.'''

    def __init__(self, session: Session):
        '''Инициализирует репозиторий цен.
        
        Args:
            session (Session): SQLAlchemy сессия для работы с БД
        '''
        self.session = session

    def save(self, price: Price) -> None:
        '''Сохраняет или обновляет цену в базе данных.
        
        Args:
            price (Price): Доменный объект цены для сохранения
            session (Session): SQLAlchemy сессия
            
        Raises:
            DatabaseError: При ошибках сохранения
        '''
        try:
            logger.info(f"Сохранение цены: {price}")
            orm_price = PriceMapper.domain_to_orm(price)
            self.session.merge(orm_price)
            logger.debug(f"Цена успешно сохранена (ID: {orm_price.id})")
        except Exception as e:
            logger.error(f"Ошибка сохранения цены {price}: {str(e)}")
            raise

    def get_relevant_price_id(self, product_id: str) -> Optional[str]:
        '''Получает ID актуальной цены для указанного продукта.
        
        Args:
            product_id (str): Идентификатор продукта
            session (Session): SQLAlchemy сессия
            
        Returns:
            Optional[str]: ID актуальной цены или None, если продукт не найден
        '''
        logger.debug(f"Получение актуальной цены для продукта {product_id}")
        orm_product = self.session.get(ORMProduct, product_id)
        if orm_product:
            logger.info(f"Актуальный price_id для продукта {product_id}: {orm_product.price_id}")
            return orm_product.price_id
        logger.warning(f"Продукт с ID {product_id} не найден")
        return None
    
    def get(self, price_id: str) -> Optional[Price]:
        '''Получает цену по её идентификатору.
        
        Args:
            price_id (str): Идентификатор цены
            session (Session): SQLAlchemy сессия
            
        Returns:
            Optional[Price]: Найденный объект цены или None
        '''
        logger.debug(f"Поиск цены по ID: {price_id}")
        orm_model = self.session.get(ORMPrice, price_id)
        if not orm_model:
            logger.warning(f"Цена с ID {price_id} не найдена")
            return None
        price = PriceMapper.orm_to_domain(orm_model)
        logger.info(f"Найдена цена: {price} (ID: {orm_model.id})")
        return price
    
    def get_prices_by_product(self, product_id: str) -> List[Price]:
        '''Получает все цены для указанного продукта.
        
        Args:
            product_id (str): Идентификатор продукта
            session (Session): SQLAlchemy сессия
            
        Returns:
            List[Price]: Список цен продукта (может быть пустым)
        '''
        logger.debug(f"Получение всех цен для продукта {product_id}")
        orm_prices = self.session.query(ORMPrice).filter_by(product_id=product_id).all()
        prices = [PriceMapper.orm_to_domain(p) for p in orm_prices]
        logger.info(f"Найдено {len(prices)} цен для продукта {product_id}")
        return prices
    
    def get_all(self, user_id: str) -> List[Price]:
        '''Получает все цены для указанного пользователя.
        
        Args:
            user_id (str): Идентификатор пользователя
            session (Session): SQLAlchemy сессия
            
        Returns:
            List[Price]: Список цен пользователя (может быть пустым)
        '''
        logger.debug(f"Получение всех цен для пользователя {user_id}")
        orm_prices = self.session.query(ORMPrice).filter_by(user_id=user_id).all()
        prices = [PriceMapper.domain_to_orm(p) for p in orm_prices]
        logger.info(f"Найдено {len(prices)} цен для пользователя {user_id}")
        return prices
    
    def delete(self, price_id: str) -> None:
        '''Удаляет цену по её идентификатору.
        
        Args:
            price_id (str): Идентификатор цены для удаления
            session (Session): SQLAlchemy сессия
            
        Raises:
            DatabaseError: При ошибках удаления
        '''
        logger.info(f"Попытка удаления цены с ID: {price_id}")
        orm_price = self.session.get(ORMPrice, price_id)
        if not orm_price:
            logger.warning(f"Цена с ID {price_id} не найдена для удаления")
            return False
        try:
            self.session.delete(orm_price)
            self.session.commit()
            logger.info(f"Цена с ID {price_id} успешно удалена")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления цены {price_id}: {str(e)}")
            raise




