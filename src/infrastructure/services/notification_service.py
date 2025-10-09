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

    async def notify_price_change(self, chat_id: str, updated_product: dict):
        """
        Отправляет уведомление пользователю об изменении цены товара.
        
        Args:
            chat_id: ID чата пользователя
            updated_product: Информация об обновлённом товаре
        """
        try:
            logger.info(f"📨 NotificationService: Отправка уведомления пользователю {chat_id}")

            new_price_with_card = updated_product['latest_price']['with_card']
            new_price_without_card = updated_product['latest_price']['without_card']

            prev_price_with_card = updated_product['latest_price']['previous_price_with_card']
            prev_price_without_card = updated_product['latest_price']['previous_price_without_card']

            price_diff = new_price_with_card - prev_price_with_card
            price_emoji = "📉" if price_diff < 0 else "📈"

            text = (
                f"{price_emoji} Цена на товар изменилась!\n\n"
                f"📦 {updated_product['name']}\n\n"
                f"💰 Актуальная цена (с картой): {new_price_with_card} ₽\n"
                f"💰 Актуальная цена (без карты): {new_price_without_card} ₽\n"             
                f"💰 Предыдущая цена (с картой): {prev_price_with_card} ₽\n"
                 f"💰 Предыдущая цена (с картой): {prev_price_without_card} ₽\n"

                f"{'💚' if price_diff < 0 else '🔴'} Разница: {price_diff:+d} ₽\n\n"
                f"🔗 {updated_product['link']}"
            )

            await self.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                disable_web_page_preview=False
            )

            logger.info(f"✅ NotificationService: Уведомление отправлено пользователю {chat_id}")

        except TelegramForbiddenError:
            logger.warning(f"⚠️ Бот заблокирован пользователем {chat_id}")

        except TelegramBadRequest as e:
            logger.error(f"❌ Некорректный запрос для чата {chat_id}: {e}")

        except TelegramAPIError as e:
            logger.error(f"❌ Ошибка Telegram API при отправке уведомления {chat_id}: {e}")
            
        except Exception as e:
            logger.exception(f"❌ Неизвестная ошибка при отправке уведомления {chat_id}: {e}")

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