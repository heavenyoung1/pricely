import logging
from sqlalchemy.orm import Session
from typing import Optional, List , TYPE_CHECKING    

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
#from src.infrastructure.database.core import with_session
from src.domain.entities import Product, Price


logger = logging.getLogger(__name__)

class PriceRepositoryImpl(PriceRepository):
    '''
    Реализация репозитория для работы с ценами в базе данных.
    
    Обеспечивает:
    - CRUD операции с ценами
    - Получение цен по продуктам и пользователям
    - Управление актуальными ценами
    '''
    def __init__(self, session: Session):
        '''Инициализирует репозиторий цен.
        
        Args:
            session (Session): SQLAlchemy сессия для работы с БД
            product_repository (ProductRepository): Репозиторий продуктов для зависимостей
        '''
        self.session = session

    def save(self, price: Price, session: Session) -> None:
        '''Сохраняет или обновляет цену в базе данных.
        
        Args:
            price (Price): Доменный объект цены для сохранения
            session (Session): SQLAlchemy сессия
            
        Raises:
            DatabaseError: При ошибках сохранения
        '''
        orm_price = PriceMapper.to_orm(price)
        session.merge(orm_price)
        logger.info(f'Цена сохранена: {price}')

    def get_relevant_price_id(self, product_id: str, session: Session) -> Optional[str]:
        '''Получает ID актуальной цены для указанного продукта.
        
        Args:
            product_id (str): Идентификатор продукта
            session (Session): SQLAlchemy сессия
            
        Returns:
            Optional[str]: ID актуальной цены или None, если продукт не найден
        '''
        orm_product = session.get(ORMProduct, product_id)
        if orm_product:
            price_id = orm_product.price_id 
            logger.info(f'Актуальный price_id для продукта {product_id}: {price_id}')
            return price_id
        logger.warning(f'Продукт с id {product_id} не найден')
        return None
    
    def get(self, price_id: str, session: Session) -> Optional[Price]:
        '''Получает цену по её идентификатору.
        
        Args:
            price_id (str): Идентификатор цены
            session (Session): SQLAlchemy сессия
            
        Returns:
            Optional[Price]: Найденный объект цены или None
        '''
        orm_price = session.get(ORMPrice, price_id)
        if orm_price:
            price = PriceMapper.to_domain(orm_price)
            logger.info(f'Цена {price} получена по id: {price_id}')
            return price
        logger.warning(f'Цена с id {price_id} не найдена')
        return None
    
    def get_prices_by_product(self, product_id: str, session: Session) -> List[Price]:
        '''Получает все цены для указанного продукта.
        
        Args:
            product_id (str): Идентификатор продукта
            session (Session): SQLAlchemy сессия
            
        Returns:
            List[Price]: Список цен продукта (может быть пустым)
        '''
        orm_prices = session.query(ORMPrice).filter(ORMPrice.product_id == product_id).all()
        prices = [PriceMapper.to_domain(orm_price) for orm_price in orm_prices]
        logger.info(f'Получено {len(prices)} цен для продукта {product_id}')
        return prices
    
    def get_all(self, user_id: str, session: Session) -> List[Price]:
        '''Получает все цены для указанного пользователя.
        
        Args:
            user_id (str): Идентификатор пользователя
            session (Session): SQLAlchemy сессия
            
        Returns:
            List[Price]: Список цен пользователя (может быть пустым)
        '''
        orm_prices = session.query(ORMPrice).filter(ORMPrice.user_id == user_id).all()
        prices = [PriceMapper.to_domain(orm_price) for orm_price in orm_prices]
        logger.info(f'Получено {len(prices)} цен для пользователя {user_id}')
        return prices
    
    def delete(self, price_id: str, session: Session) -> None:
        '''Удаляет цену по её идентификатору.
        
        Args:
            price_id (str): Идентификатор цены для удаления
            session (Session): SQLAlchemy сессия
            
        Raises:
            DatabaseError: При ошибках удаления
        '''
        orm_price = session.get(ORMPrice, price_id)
        if orm_price:
            session.delete(orm_price)
            logger.info(f'Цена удалена по id: {price_id}')
        else:
            logger.warning(f'Цена с id {price_id} не найдена')




