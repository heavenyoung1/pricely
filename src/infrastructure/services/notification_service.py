# src/infrastructure/notifications/notification_service.py
import logging
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.presentation.bot.handlers.products import _build_price_update_message

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot):
        self.bot = bot

    async def notify_price_change(self, chat_id: str, updated_product: dict, full_product: dict):
        """
        Отправляет уведомление пользователю, если изменилась цена.
        """
        try:
            text = _build_price_update_message(updated_product, full_product)
            markup = build_product_actions_keyboard(updated_product["id"], updated_product["link"])

            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=markup
            )
            logger.info(f"✅ Уведомление отправлено пользователю {chat_id} о товаре {updated_product['id']}")

        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления пользователю {chat_id}: {e}")
