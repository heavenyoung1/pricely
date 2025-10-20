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
        '''
        Инициализация репозитория для работы с товарами.

        :param session: Экземпляр SQLAlchemy Session для работы с базой данных.
        '''
        self.session = session

    def save(self, product: Product) -> None:
        '''
        Сохранить или обновить товар в базе данных.

        :param product: Объект типа Product, который необходимо сохранить или обновить.
        :raises Exception: Если возникла ошибка при сохранении товара.
        '''
        try:
            logger.info(f'Сохранение товара: {product}')
            existing = self.session.get(ORMProduct, str(product.id))

            if existing:
                # Обновляем поля существующего продукта
                existing.name = product.name
                existing.link = product.link
                existing.image_url = product.image_url
                existing.rating = product.rating
                existing.categories = product.categories
            else:
                # Создаем новый ORM продукт и добавляем его в сессию
                orm_product = ProductMapper.domain_to_orm(product)
                self.session.add(orm_product)

        except Exception as e:
            logger.error(f'Ошибка сохранения продукта {product}: {str(e)}')
            raise

    def get(self, product_id: str) -> Optional[Product]:
        '''
        Получить товар по идентификатору.

        :param product_id: Идентификатор товара.
        :return: Объект Product, если найден, иначе None.
        '''
        logger.debug(f'Поиск товара по ID: {product_id}')
        product_id = str(product_id)  # Преобразуем в строку для защиты
        orm_model = self.session.get(ORMProduct, product_id)

        if not orm_model:
            logger.warning(f'Товар с ID {product_id} не найден')
            return None
        
        # Загружаем связанные цены для товара
        orm_prices = self.session.query(ORMPrice).filter_by(product_id=product_id).all()
        prices = [PriceMapper.orm_to_domain(orm_price) for orm_price in orm_prices]
        logger.debug(f"Загружены цены для товара {product_id}: {prices}")

        # Преобразуем ORM модель товара в доменную модель
        product = ProductMapper.orm_to_domain(orm_model)
        product.prices = prices
        # ВОТ ТУТ ПОТЕНЦИАЛЬНАЯ ПРОБЛЕМА, ВОЗВРАЩАЮТСЯ ВСЕ ЦЕНЫ ДЛЯ ТОВАРА
        logger.info(f'Найден товар: {product.name} (ID: {orm_model.id})')

        return product

    # def get_all(self, user_id: str) -> List[Product]:
    #     '''
    #     Получить все товары пользователя.

    #     :param user_id: Идентификатор пользователя, чьи товары необходимо получить.
    #     :return: Список объектов Product для данного пользователя.
    #     '''
    #     logger.debug(f'Поиск всех товаров пользователя {user_id}')
    #     try:
    #         orm_models = self.session.query(ORMProduct).all()
    #         logger.debug(f'GET_ALL -> Найдены ORM модели {orm_models}')
    #         products = [ProductMapper.orm_to_domain(m) for m in orm_models]
    #         logger.info(f'Найдено {len(products)} товаров для пользователя {user_id}')
    #         return products
    #     except Exception as e:
    #         logger.error(f'Ошибка получения всех товаров пользователя {user_id}: {str(e)}')
    #         raise

    def delete(self, product_id: str) -> bool:
        '''
        Удалить товар по идентификатору.

        :param product_id: Идентификатор товара, который необходимо удалить.
        :return: Возвращает True, если товар был удален, иначе False.
        '''
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