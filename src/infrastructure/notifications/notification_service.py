import logging
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot):
        self.bot = bot

    def send_price_update_notification(self, user_id: str, product_name: str, new_price: float):
        try:
            self.bot.send_message(
                user_id,
                f"📢 Внимание! Цена на товар *{product_name}* изменилась! Теперь он стоит *{new_price} ₽*.",
                parse_mode="Markdown"
            )
            logger.info(f"Уведомление отправлено пользователю {user_id} о изменении цены на товар {product_name}.")
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления пользователю {user_id}: {e}")
