from typing import List

from aiogram import Bot

from domain.entities.notification import Notification
from domain.entities.price import Price
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from core.logger import logger


class TelegramNotificationSender:
    '''
    Сервис отправки уведомлений через Telegram.

    Отвечает за:
    - Получение chat_id пользователей
    - Форматирование сообщений об изменении цен
    - Отправку сообщений через Telegram Bot API
    '''

    def __init__(self, bot: Bot, uow_factory: UnitOfWorkFactory):
        self.bot = bot
        self.uow_factory = uow_factory

    async def send(self, notifications: List[Notification]) -> int:
        '''
        Отправляет уведомления пользователям в Telegram.

        Args:
            notifications: Список уведомлений для отправки.

        Returns:
            Количество успешно отправленных уведомлений.
        '''
        sent_count = 0

        async with self.uow_factory.create() as uow:
            for notify in notifications:
                try:
                    # Получаем chat_id пользователя
                    user = await uow.user_repo.get(notify.user_id)
                    if not user:
                        logger.warning(f'Пользователь {notify.user_id} не найден')
                        continue

                    # Получаем название товара
                    product = await uow.product_repo.get(notify.price.product_id)
                    product_name = product.name if product else 'Неизвестный товар'
                    product_link = product.link if product else None

                    # Формируем и отправляем сообщение
                    message = self._format_message(
                        product_name, notify.price, product_link
                    )
                    await self.bot.send_message(
                        chat_id=user.chat_id,
                        text=message,
                        parse_mode='HTML',
                    )

                    sent_count += 1
                    logger.info(f'Уведомление отправлено пользователю {user.chat_id}')

                except Exception as e:
                    logger.error(
                        f'Ошибка отправки уведомления user_id={notify.user_id}: {e}'
                    )

        return sent_count

    def _format_message(
        self,
        product_name: str,
        price: Price,
        product_link: str | None = None,
    ) -> str:
        '''
        Форматирует сообщение об изменении цены.

        Args:
            product_name: Название товара.
            price: Объект Price с текущей и предыдущей ценой.
            product_link: Ссылка на товар (опционально).

        Returns:
            Отформатированное HTML-сообщение.
        '''
        old_price = price.previous_with_card
        new_price = price.with_card
        diff = old_price - new_price

        if diff > 0:
            emoji = '📉'
            direction = 'снизилась'
        else:
            emoji = '📈'
            direction = 'выросла'
            diff = abs(diff)

        # Формируем название с ссылкой или без
        if product_link:
            name_line = f'📦 <a href="{product_link}">{product_name}</a>'
        else:
            name_line = f'📦 {product_name}'

        return (
            f'{emoji} <b>Цена {direction}!</b>\n\n'
            f'{name_line}\n\n'
            f'💰 Старая цена: <s>{old_price:,}</s> ₽\n'
            f'💰 Новая цена: <b>{new_price:,}</b> ₽\n'
            f'📊 Разница: {diff:,} ₽'
        )
