import logging
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot):
        self.bot = bot

    async def notify_price_change(self, chat_id: str, updated_product: dict):
        """
        Отправляет уведомление пользователю, если изменилась цена.
        """
        try:
            logger.info(f"📨 NotificationService: Отправка уведомления пользователю {chat_id}")

            text = f"🔔 Цена на товар изменилась!\n\n" \
                   f"📦 {updated_product['name']}\n\n" \
                   f"💰 Старая цена: {updated_product['latest_price']['previous_price_with_card']} ₽\n" \
                   f"💰 Новая цена: {updated_product['latest_price']['with_card']} ₽\n\n" \
                   f"🔗 {updated_product['link']}"

            await self.bot.send_message(
                chat_id=int(chat_id),
                text=text
            )

            logger.info(f"✅ NotificationService: Уведомление отправлено пользователю {chat_id}")

        except (TelegramBadRequest, TelegramAPIError) as e:
            logger.error(f"❌ NotificationService: Ошибка Telegram API: {e}")
        except Exception as e:
            logger.exception(f"❌ NotificationService: Неизвестная ошибка: {e}")