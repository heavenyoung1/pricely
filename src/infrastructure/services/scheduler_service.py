from src.infrastructure.services import product_service, NotificationService
from src.infrastructure.services.logger import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # ← ВАЖНО!
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import asyncio


class APSchedulerService:
    def __init__(self, bot, product_service, notification_service, interval_minutes=1):
        """
        Сервис планировщика (APS).
        Запускает обновление товаров и уведомления при изменении цен.
        """
        self.scheduler = AsyncIOScheduler()
        self.bot = bot
        self.product_service = product_service
        self.notification_service = notification_service
        self.interval_minutes = interval_minutes
        self.loop = None  # Сохраним ссылку на основной loop

        # Логирование результатов задач
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def start(self):
        """Запуск планировщика."""
        # Сохраняем текущий event loop
        try:
            self.loop = asyncio.get_running_loop()
            logger.info(f"📍 Scheduler использует event loop: {self.loop}")
        except RuntimeError:
            self.loop = asyncio.get_event_loop()
            logger.info(f"📍 Scheduler использует event loop (fallback): {self.loop}")
        
        self.scheduler.add_job(
            self.run_price_update, 
            'interval', 
            minutes=self.interval_minutes, 
            id="update_prices"
        )
        self.scheduler.start()
        logger.info(f"🔁 APScheduler запущен (интервал: {self.interval_minutes} мин).")

    def stop(self):
        """Остановка планировщика."""
        self.scheduler.shutdown()
        logger.info("🛑 APScheduler остановлен.")

    def listener(self, event):
        """Логирование результатов выполнения задач."""
        if event.exception:
            logger.error(f"Ошибка выполнения задачи: {event.exception}")
        else:
            logger.info("✅ ShedulerService выполнил задачу успешно.")

    async def run_price_update(self):
        """Фоновое задание для обновления цен."""
        logger.info("🚀 Запуск автоматического обновления цен...")

        try:
            users_products = self.product_service.get_all_products_for_update()
            logger.info(f'USERS_PRODUCTS ПОЛУЧЕНЫ {users_products}')

            if not users_products:
                logger.info("Нет товаров для обновления.")
                return
            
            # Храним информацию о товарах, которые будут отправлены пользователю
            notification_to_send = {}
            logger.info(f'USER_PRODUCT_ITEMS: {dict(users_products.items())}')
            for user_id, product_ids in users_products.items():
                #logger.info(f"Обрабатываем товары для пользователя {user_id}")

                # Собираем информацию для всех товаров пользователя
                updated_products = []
                logger.info(f"Обрабатываем товары для пользователя: {user_id}")
                logger.info(f"Товары для пользователя {user_id}: {product_ids}")
                for product_id in product_ids:
                    try:
                        logger.info(f'Получаем товар для обновления: ID={product_id}')

                        # Обновляем цену товара
                        result = self.product_service.update_product_price(product_id)
                        logger.info(f'Для обновления цены в Scheduler передан result: {result}')
                        product = result['updated_product']
                        logger.info(f'ПОЛУЧЕН UPDATED_PRODUCT: {product}')
                        # Флаг об изменении цены
                        is_changed = result['is_changed']
                        logger.info(f'ПОЛУЧЕН ФЛАГ is_changed: {is_changed}')

                        if is_changed:
                            updated_products.append(product)

                    except Exception as e:
                        logger.error(f"Ошибка при обработке товара {product_id}: {e}")

                if updated_products :
                    logger.info(f'⚠️  Список товаров для отправки пользователю {updated_products}')
                    notification_to_send[user_id] = updated_products

            # Отправим уведомления для всех пользователей
            for user_id, updated_products in notification_to_send.items():
                # Формируем сообщение для этого пользователя
                await self._send_notification(user_id, updated_products)

            logger.info("✅ Автоматическое обновление цен завершено.")


        except Exception as e:
            logger.error(f"Ошибка при выполнении планового обновления: {e}")

    async def _send_notification(self, chat_id: str, updated_products: list):
        """Отправка уведомления пользователю с несколькими товарами."""
        try:
            logger.info(f"📤 Попытка отправки уведомления пользователю {chat_id}")
            
            # Формируем текст сообщения с информацией о нескольких товарах
            text = "🔔 Цена на товар(ы) изменилась!\n\n"
            
            for product in updated_products:
                text += (
                    f"📦 {product['name']}\n\n"
                    f"💰 Предыдущая цена: {product['previous_price_with_card']} ₽\n"
                    f"💰 Актуальная цена: {product['with_card']} ₽\n\n"
                    f"🔗 {product['link']}\n\n"
                )
            
            logger.info(f"📝 Текст сформирован: {text[:50]}...")

            # Прямая отправка через бота
            message = await self.bot.send_message(
                chat_id=int(chat_id),
                text=text
            )
            
            logger.info(f"✅ Сообщение ID {message.message_id} отправлено пользователю {chat_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке уведомления пользователю {chat_id}: {e}", exc_info=True)
