'''
Обработчик уведомлений из Redis очереди.

Слушает очередь и отправляет уведомления пользователям через Telegram.
'''

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions

from core.logger import logger
from infrastructure.redis.message import NotificationMessage, PriceChangeItem


class NotificationHandler:
    '''Обрабатывает уведомления из Redis и отправляет в Telegram'''

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, message: NotificationMessage) -> None:
        '''
        Обработать одно уведомление.

        Args:
            message: Сообщение из Redis очереди (один пользователь, много товаров).
        '''
        try:
            text = self._format_message(message)
            keyboard = self._build_keyboard(message)
            await self.bot.send_message(
                chat_id=message.chat_id,
                text=text,
                reply_markup=keyboard,
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                parse_mode='HTML',
            )
            logger.info(
                f'Уведомление отправлено: chat_id={message.chat_id}, товаров: {len(message.items)}'
            )
        except Exception as e:
            logger.error(f'Ошибка отправки уведомления chat_id={message.chat_id}: {e}')

    def _build_keyboard(self, msg: NotificationMessage) -> InlineKeyboardMarkup | None:
        '''Строит инлайн-кнопки со ссылками на товары'''
        buttons = []
        for item in msg.items:
            if item.product_link:
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f'{item.product_name[:40]}',
                            url=item.product_link,
                        )
                    ]
                )
        if not buttons:
            return None
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    def _format_message(self, msg: NotificationMessage) -> str:
        '''Форматирует сообщение с несколькими изменёнными товарами'''
        parts = []
        for item in msg.items:
            parts.append(self._format_item(item))
        return '\n\n━━━━━━━━━━━━━━━\n\n'.join(parts)

    def _format_item(self, item: PriceChangeItem) -> str:
        '''Форматирует один товар с изменённой ценой'''
        old_price = item.previous_with_card
        new_price = item.price_with_card
        diff = old_price - new_price

        if diff > 0:
            emoji = '📉'
            direction = 'снизилась'
        else:
            emoji = '📈'
            direction = 'выросла'
            diff = abs(diff)

        if item.product_link:
            name_line = f'📦 <a href="{item.product_link}">{item.product_name}</a>'
        else:
            name_line = f'📦 {item.product_name}'

        return (
            f'{emoji} <b>Цена {direction}!</b>\n\n'
            f'{name_line}\n\n'
            f'💰 Старая цена: <s>{old_price:,}</s> ₽\n'
            f'💰 Новая цена: <b>{new_price:,}</b> ₽\n'
            f'📊 Разница: {diff:,} ₽'
        )
