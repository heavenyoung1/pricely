# from adapters.interfaces import INotifier
# from models import Product
# from telegram import Bot

# class TelegramNotifier(INotifier):
#     def __init__(self, bot_token: str):
#         self.bot = Bot(token=bot_token)

#     async def notify(self, chat_id: int, product: Product, old_price: float) -> None:
#         message = (
#             f"Цена изменилась!\n"
#             f"Товар: {product.name}\n"
#             f"Старая цена: {old_price:.2f} ₽\n"
#             f"Новая цена: {product.price:.2f} ₽\n"
#             f"Ссылка: {product.url}"
#         )
#         await self.bot.send_message(chat_id=chat_id, text=message)