import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from src.application.interfaces.repositories import ProductRepository
from src.infrastructure.database.mappers import ProductMapper, PriceMapper
from src.domain.entities import Product 
from src.infrastructure.database.models import ORMProduct, ORMPrice


logger = logging.getLogger(__name__)

class ProductRepositoryImpl(ProductRepository):
    '''Реализация репозитория для работы с товарами в базе данных.'''
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> None:
        try:
            logger.info(f'Сохранение товара: {product}')
            existing = self.session.get(ORMProduct, str(product.id))

            if existing:
                # обновляем поля
                existing.name = product.name
                existing.link = product.link
                existing.image_url = product.image_url
                existing.rating = product.rating
                existing.categories = product.categories
            else:
                orm_product = ProductMapper.domain_to_orm(product)
                self.session.add(orm_product)

        except Exception as e:
            logger.error(f'Ошибка сохранения продукта {product}: {str(e)}')
            raise

    def get(self, product_id: str) -> Optional['Product']:
        '''Получает товар по ID.'''
        logger.debug(f'Поиск товар по ID: {product_id}')
        product_id = str(product_id)  # защита
        orm_model = self.session.get(ORMProduct, product_id)
        if not orm_model:
            logger.warning(f'Товар с ID {product_id} не найден')
            return None
        
        # Загружаем связанные цены
        orm_prices = (
            self.session.query(ORMPrice).filter_by(product_id=product_id).all())
        prices = [PriceMapper.orm_to_domain(orm_price) for orm_price in orm_prices]
        logger.debug(f"Loaded prices for product {product_id}: {prices}")

        product = ProductMapper.orm_to_domain(orm_model)
        product.prices = prices
        logger.info(f'Найден Товар: {product} (ID: {orm_model.id})')
        return product
    
    def get_all(self, user_id: str) -> List['Product']:
        '''Получает все товары пользователя.'''
        logger.debug(f'Поиск всех товаров пользователя {user_id}')
        try:
            orm_models = self.session.query(ORMProduct).all()
            logger.debug(f'GET_ALL -> НАЙДЕНЫ ORM_MODELS {orm_models}')
            products = [ProductMapper.orm_to_domain(m) for m in orm_models]
            logger.info(f'Найдено {len(products)} товаров для пользователя {user_id}')
            return products
        except Exception as e:
            logger.error(f'Ошибка получения всех товаров пользователя {user_id}: {str(e)}')
            raise

    def delete(self, product_id: str) -> bool:
        '''Удаляет товар по ID.'''
        logger.info(f'Попытка удаления товара с ID: {product_id}')
        orm_model = self.session.get(ORMProduct, product_id)
        if not orm_model:
            logger.warning(f'Товар с ID {product_id} не найден для удаления')
            return False
        try:
            self.session.delete(orm_model)
            logger.info(f'Товар с ID {product_id} успешно удален')
            return True
        except Exception as e:
            logger.error(f'Ошибка удаления товара {product_id}: {str(e)}')
            raise

