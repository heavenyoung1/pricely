import logging
from typing import Optional, List, TYPE_CHECKING

from src.domain.repositories import ProductRepository
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMProduct
from src.infrastructure.database.core import with_session
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from src.domain.entities import Product 

logger = logging.getLogger(__name__)

class ProductRepositoryImpl(ProductRepository):
    '''Реализация репозитория для работы с продуктами в базе данных.'''
    
    def __init__(self, session: Session):
        '''
        Инициализация репозитория.
        
        Args:
            session: SQLAlchemy Session для работы с БД
        '''
        self.session = session

    @with_session
    def save(self, product) -> None:
        '''
        Сохраняет продукт в базу данных.
        
        Args:
            product: Доменный объект продукта для сохранения
            
        Raises:
            DatabaseError: При ошибках работы с БД
        '''
        try:
            logger.info(f'Сохранение продукта: {product}')
            orm_product = ProductMapper.to_orm(product)
            self.session.merge(orm_product)
            logger.debug(f'Продукт успешно сохранен (ID: {orm_product.id})')
        except Exception as e:
            logger.error(f'Ошибка сохранения продукта {product}: {str(e)}')
            raise

    @with_session
    def get(self, product_id: int) -> Optional['Product']:
        '''
        Получает продукт по его ID.
        
        Args:
            product_id: Идентификатор продукта
            
        Returns:
            Optional[Product]: Найденный продукт или None если не найден
        '''
        logger.debug(f'Поиск продукта по ID: {product_id}')
        orm_model = self.session.get(ORMProduct, product_id)
        
        if not orm_model:
            logger.warning(f'Продукт с ID {product_id} не найден')
            return None
        
        product = ProductMapper.to_domain(orm_model)
        logger.info(f'Найден продукт: {product} (ID: {orm_model.id})')
        return product

    @with_session
    def delete(self, product_id: int) -> bool:
        '''
        Удаляет продукт по его ID.
        
        Args:
            product_id: Идентификатор продукта для удаления
            
        Returns:
            bool: True если удаление успешно, False если продукт не найден
        '''
        logger.info(f'Попытка удаления продукта с ID: {product_id}')
        orm_model = self.session.get(ORMProduct, product_id)
        
        if not orm_model:
            logger.warning(f'Продукт с ID {product_id} не найден для удаления')
            return False
            
        try:
            self.session.delete(orm_model)
            logger.info(f'Продукт с ID {product_id} успешно удален')
            return True
        except Exception as e:
            logger.error(f'Ошибка удаления продукта {product_id}: {str(e)}')
            raise

    @with_session
    def get_all(self, user_id: int) -> List['Product']:

        '''
        Получает все продукты для указанного пользователя.
        
        Args:
            user_id: Идентификатор пользователя
            
        Returns:
            List[Product]: Список продуктов пользователя (может быть пустым)
        '''
        logger.debug(f'Поиск всех продуктов пользователя {user_id}')
        try:
            orm_models = self.session.query(ORMProduct).filter_by(user_id=user_id).all()
            products = [ProductMapper.to_domain(m) for m in orm_models]
            logger.info(f'Найдено {len(products)} продуктов для пользователя {user_id}')
            return products
        except Exception as e:
            logger.error(f'Ошибка получения продуктов пользователя {user_id}: {str(e)}')
            raise