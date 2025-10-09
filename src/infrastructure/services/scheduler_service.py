from src.infrastructure.services import product_service, NotificationService
from src.infrastructure.services.logger import logger
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.presentation.bot.handlers.products import _build_price_update_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import asyncio


class APSchedulerService:
    def __init__(self, bot, product_service, notification_service, interval_minutes=1):
        """
        Сервис планировщика (APS).
        Запускает обновление товаров и уведомления при изменении цен.
        """
        self.scheduler = BackgroundScheduler()
        self.bot = bot
        self.product_service = product_service
        self.notification_service = notification_service
        self.interval_minutes = interval_minutes

        # Логирование результатов задач
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def start(self):
        """Запуск планировщика."""
        self.scheduler.add_job(self.run_price_update, 'interval', minutes=self.interval_minutes, id="update_prices")
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

    def run_price_update(self):
        """Фоновое задание для обновления цен."""
        logger.info("🚀 Запуск автоматического обновления цен...")

        try:
            # Создаём новый event loop для этого потока
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Запускаем асинхронную функцию
                loop.run_until_complete(self._async_price_update())
            finally:
                loop.close()

            logger.info("✅ Автоматическое обновление цен завершено.")

        except Exception as e:
            logger.error(f"Ошибка при выполнении планового обновления: {e}", exc_info=True)

    async def _async_price_update(self):
        """Асинхронная часть обновления цен."""
        users_products = self.product_service.get_all_products_for_update()

        if not users_products:
            logger.info("Нет товаров для обновления.")
            return

        for user_product in users_products:
            try:
                product_id = user_product['product_id']
                user_id = user_product['user_id']
                
                logger.info(f'Извлечен user:product -> {user_product}')
                logger.info(f'Получен товар для обновления: ID={product_id}')
                
                # Обновляем цену товара
                result = self.product_service.update_product_price(product_id)
                
                logger.info(f"Результат обновления для товара {product_id}: is_changed={result.get('is_changed')}")

                # Проверяем, что результат содержит нужные данные
                if not result or 'full_product' not in result:
                    logger.warning(f"Некорректный результат для товара {product_id}: {result}")
                    continue
                
                full_product = result["full_product"]
                
                # ========================================
                # ТЕСТОВЫЙ РЕЖИМ: отправляем всегда
                # ========================================
                logger.info(f"🧪 ТЕСТ: Принудительная отправка уведомления пользователю {user_id}")
                await self._send_notification(user_id, full_product)
                
                # ========================================
                # ПРОДАКШЕН КОД (раскоммент когда тест пройдёт):
                # ========================================
                # if result.get("is_changed", False):
                #     logger.info(f"🔔 Цена изменилась для товара {product_id}, отправка уведомления пользователю {user_id}")
                #     await self._send_notification(user_id, full_product)
                # else:
                #     logger.info(f"Цена не изменилась для товара {product_id}")
                
                # Обрабатываем только первый товар для теста
                logger.info("🧪 ТЕСТ: Остановка после первого товара")
                break
                    
            except Exception as e:
                logger.error(f"Ошибка при обработке товара {user_product.get('product_id', 'unknown')}: {e}", exc_info=True)
                continue

    async def _send_notification(self, chat_id: str, full_product: dict):
        """Отправка уведомления в отдельной задаче."""
        try:
            logger.info(f"📤 Попытка отправки уведомления пользователю {chat_id}")
            logger.info(f"📦 Данные товара: {full_product}")
            
            await self.notification_service.notify_price_change(
                chat_id=chat_id,
                updated_product=full_product,
                #full_product=full_product
            )
            logger.info(f"✅ Уведомление успешно отправлено пользователю {chat_id}")
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке уведомления пользователю {chat_id}: {e}", exc_info=True)

