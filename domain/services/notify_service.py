from typing import List

from domain.entities.notification import Notification

'''
Обработчик уведомлений из Redis очереди.

Слушает очередь и отправляет уведомления пользователям через Telegram.
'''

from aiogram import Bot

from core.logger import logger
from infrastructure.redis.message import NotificationMessage


class NotificationHandler:
    '''Обрабатывает уведомления из Redis и отправляет в Telegram'''

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: NotificationMessage) -> None:
        '''
        Обработать одно уведомление.

        Args:
            message: Сообщение из Redis очереди.
        '''
        try:
            text = self._format_message(message)
            await self.bot.send_message(
                chat_id=message.chat_id,
                text=text,
                parse_mode='HTML',
            )
            logger.info(f'Уведомление отправлено: chat_id={message.chat_id}')
        except Exception as e:
            logger.error(f'Ошибка отправки уведомления chat_id={message.chat_id}: {e}')

    async def _build_messages(
        self, notifications: List[Notification]
    ) -> List[NotificationMessage]:
        '''
        Собирает полные данные для уведомлений.

        Обогащает уведомления данными из БД (chat_id, product info),
        чтобы бот мог отправить сообщение без обращения к БД.
        '''
        messages = []

        async with self.uow_factory.create() as uow:
            for notify in notifications:
                # Получаем chat_id пользователя
                user = await uow.user_repo.get(notify.user_id)
                if not user:
                    logger.warning(f'Пользователь {notify.user_id} не найден')
                    continue

                # Получаем информацию о товаре
                product = await uow.product_repo.get(notify.price.product_id)
                if not product:
                    logger.warning(f'Товар {notify.price.product_id} не найден')
                    continue

                message = NotificationMessage(
                    chat_id=user.chat_id,
                    product_name=product.name,
                    product_link=product.link,
                    price_with_card=notify.price.with_card,
                    price_without_card=notify.price.without_card,
                    previous_with_card=notify.price.previous_with_card,
                    previous_without_card=notify.price.previous_without_card,
                )
                messages.append(message)

        return messages

    def _format_message(self, msg: NotificationMessage) -> str:
        '''Форматирует сообщение об изменении цены'''
        old_price = msg.previous_with_card
        new_price = msg.price_with_card
        diff = old_price - new_price

        if diff > 0:
            emoji = '📉'
            direction = 'снизилась'
        else:
            emoji = '📈'
            direction = 'выросла'
            diff = abs(diff)

        # Формируем название с ссылкой или без
        if msg.product_link:
            name_line = f'📦 <a href="{msg.product_link}">{msg.product_name}</a>'
        else:
            name_line = f'📦 {msg.product_name}'

        return (
            f'{emoji} <b>Цена {direction}!</b>\n\n'
            f'{name_line}\n\n'
            f'💰 Старая цена: <s>{old_price:,}</s> ₽\n'
            f'💰 Новая цена: <b>{new_price:,}</b> ₽\n'
            f'📊 Разница: {diff:,} ₽'
        )
