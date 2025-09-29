import logging
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot):
        self.bot = bot

    def send_price_update_notification(self, user_id: str, product_name: str, old_price: float, new_price: float):
        try:
            self.bot.send_message(
                user_id,
                f"📢 Цена изменилась!\n\n"
                f"<b>{product_name}</b>\n"
                f"{old_price} ₽ → {new_price} ₽",
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления {user_id}: {e}")
