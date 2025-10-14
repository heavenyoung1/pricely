import logging
import asyncio
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

class NotificationService:
    '''
    Сервис для отправки уведомлений пользователям через Telegram бота.
    '''
    
    def __init__(self, bot):
        '''
        Инициализация сервиса уведомлений.
        
        Args:
            bot: Экземпляр бота aiogram
        '''
        self.bot = bot


    async def notify_multiple_products(self, chat_id: str, updated_products: list):
        '''
        Отправляет уведомление нескольким товарам пользователю.
        
        Args:
            chat_id: ID чата пользователя
            updated_products: Список товаров с обновленными ценами
        '''
        try:
            logger.info(f'📨 NotificationService: Отправка уведомления пользователю {chat_id}')

            # Формируем текст сообщения с информацией о нескольких товарах
            products_count = len(updated_products)
            product_word = get_product_word_form(products_count)  # Получаем правильную форму слова

            text = f'🔔 {"Цена на " + product_word if products_count == 1 else f"Цены на {products_count} {product_word} изменились"}!\n\n'
            footer = f'\n{"—" * 25}\n\n'  # Разделитель между товарами

            # Создание клавиатуры
            inline_buttons = []  # Список кнопок для клавиатуры

            for i, product in enumerate(updated_products):
                new_price_with_card = product['with_card']
                new_price_without_card = product['without_card']
                prev_price_with_card = product['previous_price_with_card']
                prev_price_without_card = product['previous_price_without_card']
                price_diff = new_price_with_card - prev_price_with_card
                price_emoji = '📉' if price_diff < 0 else '📈'

                # Формируем текст для каждого товара
                text += (
                    f'{price_emoji} 📦 [*{product["name"][:50]}*]({product["link"]})\n\n'
                    f'💳 Актуальная цена: **{new_price_with_card} ₽**\n'
                    f'💳 Предыдущая цена: **{prev_price_with_card} ₽**\n'
                    f'{"💚" if price_diff < 0 else "🔴"} **Разница**: {price_diff:+d} ₽\n\n'
                )

                # Если это не последний элемент, добавляем разделитель
                if i != len(updated_products) - 1:
                    text += footer

                # Добавляем кнопку для товара в клавиатуру
                button = InlineKeyboardButton(text=f'{product["name"][:50]}', url=product['link'])
                inline_buttons.append([button])  # Добавляем кнопку в список как отдельный элемент

            # Создаем клавиатуру с кнопками
            keyboard = InlineKeyboardMarkup(inline_keyboard=inline_buttons)

            logger.info(f'📝 Текст сформирован: {text[:50]}...')

            # Прямая отправка через бота
            message = await self.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                parse_mode='Markdown',  # Указываем, что формат будет Markdown
                disable_web_page_preview=True,  # Отключаем предпросмотр ссылок
                reply_markup=keyboard,  # Прикрепляем клавиатуру
            )
            
            logger.info(f'✅ Сообщение ID {message.message_id} отправлено пользователю {chat_id}')
        
        except Exception as e:
            logger.error(f'❌ Ошибка при отправке уведомления пользователю {chat_id}: {e}', exc_info=True)


    async def notify_multiple_users(self, users_chat_ids: list, updated_product: dict):
        '''
        Отправляет уведомления нескольким пользователям.
        
        Args:
            users_chat_ids: Список ID чатов пользователей
            updated_product: Информация об обновлённом товаре
        '''
        for chat_id in users_chat_ids:
            await self.notify_price_change(chat_id, updated_product)
            # Небольшая задержка между отправками, чтобы не попасть под rate limit
            await asyncio.sleep(0.3)

def get_product_word_form(count):
    if count == 1:
        return 'товар'
    elif 2 <= count <= 4:
        return 'товара'
    else:
        return 'товаров'
