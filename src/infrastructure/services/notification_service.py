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
            logger.info(f"🔔 NotificationService: Начало отправки уведомления пользователю {chat_id}")
            logger.info(f"📦 NotificationService: Данные товара: {updated_product}")
            
            # Формируем текст сообщения
            text = _build_price_update_message(updated_product, full_product)
            logger.info(f"📝 NotificationService: Сформирован текст: {text[:100]}...")
            
            # Формируем клавиатуру
            markup = build_product_actions_keyboard(updated_product["id"], updated_product["link"])
            logger.info(f"⌨️ NotificationService: Клавиатура создана")

            # Отправляем сообщение
            logger.info(f"🚀 NotificationService: Отправка сообщения через bot.send_message...")
            await self.bot.send_message(
                chat_id=int(chat_id),
                text=text,
                reply_markup=markup,
                parse_mode="HTML"
            )
            
            logger.info(f"✅ NotificationService: Уведомление отправлено пользователю {chat_id} о товаре {updated_product['id']}")

        except Exception as e:
            logger.error(f"❌ NotificationService: Ошибка при отправке уведомления пользователю {chat_id}: {e}", exc_info=True)