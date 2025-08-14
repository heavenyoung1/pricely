import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from src.domain.repositories import ProductRepository
from src.infrastructure.mappers import ProductMapper
from src.domain.entities import Product 
from src.infrastructure.database.models import ORMProduct


logger = logging.getLogger(__name__)

class ProductRepositoryImpl(ProductRepository):
    '''Реализация репозитория для работы с товарами в базе данных.'''
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> None:
        try:
            logger.info(f'Сохранение товара: {product}')
            orm_product = ProductMapper.domain_to_orm(product)
            self.session.merge(orm_product)
            logger.debug(f'Товар успешно сохранен (ID: {orm_product.id})')
        except Exception as e:
            logger.error(f'Ошибка сохранения продукта {product}: {str(e)}')
            raise

    def get(self, product_id: str) -> Optional['Product']:
        '''Получает товар по ID.'''
        logger.debug(f'Поиск товар по ID: {product_id}')
        orm_model = self.session.get(ORMProduct, product_id)
        if not orm_model:
            logger.warning(f'Товар с ID {product_id} не найден')
            return None
        product = ProductMapper.domain_to_orm(orm_model)
        logger.info(f'Найден Товар: {product} (ID: {orm_model.id})')
        return product

    def delete(self, product_id: str) -> bool:
        '''Удаляет товар по ID.'''
        logger.info(f'Попытка удаления товара с ID: {product_id}')
        orm_model = self.session.get(ORMProduct, product_id)
        if not orm_model:
            logger.warning(f'Товар с ID {product_id} не найден для удаления')
            return False
        try:
            self.session.delete(orm_model)
            #self.session.commit() # БЕЗ НЕГО НЕ РАБОТАЕТ, НО МНЕ НУЖНО ЦЕНТРАЛИЗОВАННОЕ УПРАВЛЕНИЕ ТРАНЗАКЦИЯМИ!!!
            logger.info(f'Товар с ID {product_id} успешно удален')
            return True
        except Exception as e:
            logger.error(f'Ошибка удаления товара {product_id}: {str(e)}')
            raise

    def get_all(self, user_id: str) -> List['Product']:
        '''Получает все товары пользователя.'''
        logger.debug(f'Поиск всех товаров пользователя {user_id}')
        try:
            orm_models = self.session.query(ORMProduct).filter_by(user_id=user_id).all()
            products = [ProductMapper.domain_to_orm(m) for m in orm_models]
            logger.info(f'Найдено {len(products)} товаров для пользователя {user_id}')
            return products
        except Exception as e:
            logger.error(f'Ошибка получения товаров пользователя {user_id}: {str(e)}')
            raise