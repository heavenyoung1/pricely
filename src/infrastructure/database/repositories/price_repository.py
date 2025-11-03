import logging
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.application.interfaces.repositories import PriceRepository
from src.infrastructure.database.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

logger = logging.getLogger(__name__)


class PriceRepositoryImpl(PriceRepository):
    """Реализация репозитория для работы с ценами в базе данных."""

    def __init__(self, session: Session):
        """
        Конструктор для инициализации репозитория цен.

        :param session: Экземпляр SQLAlchemy Session для работы с базой данных.
        """
        self.session = session

    def save(self, price: Price) -> None:
        """
        Сохранить или обновить цену в базе данных.

        :param price: Объект типа Price, который необходимо сохранить.
        :raises Exception: Если возникла ошибка при сохранении цены.
        """
        try:
            logger.info(f"Сохранение цены: {price}")
            # Преобразуем доменный объект Price в ORM-объект
            orm_price = PriceMapper.domain_to_orm(price)
            # Используем merge для объединения изменений (если объект уже существует, он обновится)
            self.session.merge(orm_price)  # Используется merge для гибкости обновления
            logger.debug(f"Цена успешно сохранена (ID: {orm_price.id})")
        except Exception as e:
            logger.error(f"Ошибка сохранения цены {price}: {str(e)}")
            raise

    def get(self, price_id: str) -> Optional[Price]:
        """
        Получить цену по идентификатору из базы данных.

        :param price_id: Идентификатор цены.
        :return: Объект Price, если найден, иначе None.
        """
        orm_model = self.session.get(ORMPrice, price_id)

        if not orm_model:
            logger.warning(f"Цена с ID {price_id} не найдена")
            return None

        price = PriceMapper.orm_to_domain(orm_model)
        logger.info(f"Найдена цена: {price} (ID: {orm_model.id})")
        return price

    def get_all_prices_by_product(self, product_id: str) -> List[Price]:
        """
        Получить все цены для конкретного продукта.

        :param product_id: Идентификатор продукта.
        :return: Список объектов Price для данного продукта.
        """
        logger.debug(f"Получение всех цен для продукта {product_id}")
        try:
            orm_prices = (
                self.session.query(ORMPrice).filter_by(product_id=product_id).all()
            )
            prices = [PriceMapper.orm_to_domain(p) for p in orm_prices]
            logger.info(f"Найдено {len(prices)} цен для продукта {product_id}")
            return prices
        except Exception as e:
            logger.error(f"Ошибка получения цен для продукта {product_id}: {str(e)}")
            raise

    def delete(self, price_id: str) -> bool:
        """
        Удалить цену по идентификатору.

        :param price_id: Идентификатор цены, которую нужно удалить.
        :return: Возвращает True, если цена была удалена, иначе False.
        """
        logger.info(f"Попытка удаления цены с ID: {price_id}")
        orm_price = self.session.get(ORMPrice, price_id)

        if not orm_price:
            logger.warning(f"Цена с ID {price_id} не найдена для удаления")
            return False
        try:
            self.session.delete(orm_price)
            logger.info(f"Цена с ID {price_id} успешно удалена")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления цены {price_id}: {str(e)}")
            raise

    def get_latest_for_product(self, product_id: str) -> Price | None:
        """
        Получить последнюю цену по времени для продукта.

        :param product_id: Идентификатор продукта.
        :return: Объект Price, если цена найдена, иначе None.
        """
        logger.debug(f"Получение последней цены для продукта {product_id}")
        orm_price = (
            self.session.query(ORMPrice)
            .filter(ORMPrice.product_id == product_id)
            .order_by(desc(ORMPrice.created_at))
            .first()
        )

        if not orm_price:
            logger.info(f"Для продукта {product_id} нет данных о цене")
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

    def delete_all_prices_for_product(self, product_id: str) -> bool:
        """
        Удалить все цены для товара по product_id.

        :param product_id: Идентификатор товара, для которого нужно удалить все связанные цены.
        :return: Возвращает True, если цены были удалены, иначе False.
        """
        logger.info(f"Попытка удаления всех цен для товара с ID: {product_id}")

        try:
            # Получаем все цены для указанного товара
            orm_prices = (
                self.session.query(ORMPrice)
                .filter(ORMPrice.product_id == product_id)
                .all()
            )

            # Если нет цен для данного товара, то возвращаем False
            if not orm_prices:
                logger.warning(f"Нет цен для товара с ID {product_id} для удаления")
                return False

            # Удаляем все найденные цены
            for orm_price in orm_prices:
                self.session.delete(orm_price)

            logger.info(f"Все цены для товара с ID {product_id} успешно удалены")
            return True
        except Exception as e:
            logger.error(f"Ошибка удаления цен для товара {product_id}: {str(e)}")
            raise
