from typing import List

from infrastructure.database.unit_of_work import UnitOfWorkFactory

from domain.interfaces.parser import IProductParser
from domain.entities.price import Price
from core.logger import logger


class CheckPriceUseCase:
    '''
    Use Case для проверки актуальных цен товаров.

    Парсит текущие цены, сравнивает с БД и сохраняет изменения,
    если цена изменилась больше чем на заданный процент (change).
    '''

    def __init__(
        self,
        parser: IProductParser,
        uow_factory: UnitOfWorkFactory,
    ) -> None:
        self.parser = parser
        self.uow_factory = uow_factory

    async def execute(self, urls: List[str]) -> List[Price]:
        '''
        Проверяет цены для списка URL.

        Args:
            urls: Список URL товаров для проверки.

        Returns:
            Список Price с изменившимися ценами.
        '''
        parsed = await self.parser.fetch_current_prices(urls)
        changed_prices = []

        async with self.uow_factory.create() as uow:
            for parsed_product in parsed:
                url = parsed_product.url
                current_price_with_card = parsed_product.price_with_card
                current_price_without_card = parsed_product.price_without_card

                # 1. Ищем товар по ссылке
                product = await uow.product_repo.get_by_link(url)
                if not product:
                    logger.warning(f'Товар с URL {url} не найден в БД')
                    continue

                # 2. Получаем цены из БД
                price_from_db = await uow.price_repo.get_actual(product.id)
                price_with = price_from_db.with_card
                price_without = price_from_db.without_card

                # 3. Вычисляем минимальную разницу для уведомления
                change = product.change
                percent = change / 100
                min_difference = percent * price_with

                # 4. Проверяем, изменилась ли цена больше чем на change%
                price_diff = abs(price_with - current_price_with_card)
                if price_diff > min_difference:
                    new_price = Price.create(
                        product_id=product.id,
                        with_card=current_price_with_card,
                        without_card=current_price_without_card,
                        previous_with_card=price_with,
                        previous_without_card=price_without,
                    )
                    await uow.price_repo.save(new_price)
                    changed_prices.append(new_price)

                    direction = '↓' if current_price_with_card < price_with else '↑'
                    logger.info(
                        f'Цена изменилась {direction}: {product.name} ({price_with} → {current_price_with_card})'
                    )

        return changed_prices
