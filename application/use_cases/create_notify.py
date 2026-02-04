from collections import defaultdict
from typing import List

from domain.entities.notification import Notification
from domain.entities.price import Price
from domain.entities.user_products import UserProducts


class CreateNotifyUseCase:
    async def execute(
        self,
        changed_price: List[Price],
        user_links: List[UserProducts],
    ) -> List[Notification]:
        '''
        Формирует список уведомлений для пользователей об изменении цен.

        Сопоставляет изменённые цены с пользователями через product_id.
        Каждый пользователь получает уведомление для каждого отслеживаемого
        товара, цена которого изменилась.

        Args:
            changed_price: Список цен товаров, которые изменились.
            user_links: Список связей пользователь-товар.

        Returns:
            Список уведомлений для отправки пользователям.
        '''
        # 1. Индекс: product_id → [user_id, ...]
        product_to_users = defaultdict(list)
        for link in user_links:
            product_to_users[link.product_id].append(link.user_id)

        # 2. Формируем уведомления
        notifications = []
        for price in changed_price:
            for user_id in product_to_users.get(price.product_id, []):
                notifications.append(Notification(user_id=user_id, price=price))

        return notifications
