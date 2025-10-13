import logging
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest, TelegramForbiddenError
import asyncio

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Сервис для отправки уведомлений пользователям через Telegram бота.
    """
    
    def __init__(self, bot):
        """
        Инициализация сервиса уведомлений.
        
        Args:
            bot: Экземпляр бота aiogram
        """
        self.bot = bot


    async def notify_multiple_products(self, chat_id: str, updated_products: list):
        """Отправка уведомлений с несколькими товарами."""
        try:
            logger.info(f"📨 NotificationService: Отправка уведомления пользователю {chat_id}")

            # Формируем текст сообщения с информацией о нескольких товарах
            text = "🔔 Цена на товар(ы) изменилась!\n\n"

            for product in updated_products:
                new_price_with_card = product['with_card']
                new_price_without_card = product['without_card']
                prev_price_with_card = product['previous_price_with_card']
                prev_price_without_card = product['previous_price_without_card']
                price_diff = new_price_with_card - prev_price_with_card
                price_emoji = "📉" if price_diff < 0 else "📈"

                text += (
                    f"{price_emoji} 📦 {product['name']}\n\n"
                    f"💰 Актуальная цена (с картой): {new_price_with_card} ₽\n"
                    f"💰 Актуальная цена (без карты): {new_price_without_card} ₽\n"             
                    f"💰 Предыдущая цена (с картой): {prev_price_with_card} ₽\n"
                    f"💰 Предыдущая цена (без карты): {prev_price_without_card} ₽\n"
                    f"{'💚' if price_diff < 0 else '🔴'} Разница: {price_diff:+d} ₽\n\n"
                    f"[Ссылка на товар]({product['link']})\n"
                    f"\n{'—' * 20}\n\n"  # Разделитель между товарами
                )

            logger.info(f"📝 Текст сформирован: {text[:50]}...")

            # Прямая отправка через бота
            message = await self.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                disable_web_page_preview=True  # Отключаем предпросмотр ссылок
            )
            
            logger.info(f"✅ Сообщение ID {message.message_id} отправлено пользователю {chat_id}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке уведомления пользователю {chat_id}: {e}", exc_info=True)

    async def notify_multiple_users(self, users_chat_ids: list, updated_product: dict):
        """
        Отправляет уведомления нескольким пользователям.
        
        Args:
            users_chat_ids: Список ID чатов пользователей
            updated_product: Информация об обновлённом товаре
        """
        for chat_id in users_chat_ids:
            await self.notify_price_change(chat_id, updated_product)
            # Небольшая задержка между отправками, чтобы не попасть под rate limit
            await asyncio.sleep(0.3)