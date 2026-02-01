from typing import List, Dict, Any

from domain.entities.price import Price
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from core.logger import logger


class UpdatePricesUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
            self,
            parsed_items: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        '''
        Принимает результат парсера:
        [
            {
                'chat_id': 123,
                'url': 'https://ozon.ru/...',
                'article': '12345',
                'name': 'Товар',
                'price_with_card': 1000,
                'price_without_card': 1200,
            },
            ...
        ]

        Возвращает список изменений для уведомлений:
        [
            {
                'chat_id': 123,
                'name': 'Товар',
                'url': 'https://ozon.ru/...',
                'old_price': 1500,
                'new_price': 1000,
                'old_price_without_card': 1800,
                'new_price_without_card': 1200,
            },
            ...
        ]
        '''
        changes = []

        async with self.uow_factory.create() as uow:
            for item in parsed_items:
                url = item.get('url')
                new_with_card = item.get('price_with_card')
                new_without_card = item.get('price_without_card')

                if new_with_card is None or new_without_card is None:
                    logger.warning(f'Пропуск {url}: цена не распарсилась')
                    continue

                # 1. Ищем товар по ссылке
                product = await uow.product_repo.get_by_link(url)
                if not product:
                    logger.warning(f'Товар с URL {url} не найден в БД')
                    continue

                # 2. Получаем текущую цену
                current_price = await uow.price_repo.get_actual(product.id)

                # 3. Определяем предыдущие значения
                if current_price:
                    prev_with = current_price.with_card
                    prev_without = current_price.without_card
                else:
                    prev_with = new_with_card
                    prev_without = new_without_card

                # 4. Сохраняем новую цену
                new_price = Price.create(
                    product_id=product.id,
                    with_card=new_with_card,
                    without_card=new_without_card,
                    previous_with_card=prev_with,
                    previous_without_card=prev_without,
                )
                await uow.price_repo.save(new_price)

                # 5. Если цена изменилась — добавляем в список уведомлений
                if current_price and (
                    new_with_card != current_price.with_card
                    or new_without_card != current_price.without_card
                ):
                    changes.append({
                        'chat_id': item.get('chat_id'),
                        'name': product.name,
                        'url': url,
                        'old_price': current_price.with_card,
                        'new_price': new_with_card,
                        'old_price_without_card': current_price.without_card,
                        'new_price_without_card': new_without_card,
                    })

                    logger.info(
                        f'Цена изменилась: {product.name} '
                        f'{current_price.with_card} -> {new_with_card}'
                    )

        return changes
