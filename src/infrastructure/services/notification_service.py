# src/infrastructure/notifications/notification_service.py
import logging
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.presentation.bot.handlers.products import _build_price_update_message
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
import asyncio

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot):
        self.bot = bot

    async def notify_price_change(self, chat_id: str, updated_product: dict):
        """
        Отправляет уведомление пользователю, если изменилась цена.
        """
        try:
            logger.info(f"📨 Отправка уведомления пользователю {chat_id}")
            logger.info(f"📦 updated_product = {updated_product}")

            # Формируем сообщение
            text = f"Цена на товар '{updated_product['name']}' изменилась!\n" \
                   f"Старая цена: {updated_product['latest_price']['previous_price_with_card']}\n" \
                   f"Новая цена: {updated_product['latest_price']['with_card']}\n" \
                   f"Ссылка: {updated_product['link']}"

            # Отправляем сообщение
            await self.bot.send_message(
                chat_id=str(chat_id),
                text=text,
                parse_mode="HTML"
            )

            logger.info(f"✅ Уведомление успешно отправлено пользователю {chat_id} по товару {updated_product['id']}")

        except TelegramBadRequest as e:
            # Например, если бот заблокирован пользователем
            logger.warning(f"⚠️ TelegramBadRequest для чата {chat_id}: {e}")
        except TelegramAPIError as e:
            logger.error(f"❌ Ошибка Telegram API при уведомлении {chat_id}: {e}")
        except Exception as e:
            logger.exception(f"❌ Неизвестная ошибка при отправке уведомления {chat_id}: {e}")