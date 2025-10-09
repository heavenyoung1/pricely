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

                    if not result or 'full_product' not in result:
                        logger.warning(f"Некорректный результат для товара {product_id}")
                        continue
                    
                    full_product = result["full_product"]
                    
                    # ТЕСТОВЫЙ РЕЖИМ: отправляем всегда
                    logger.info(f"🧪 ТЕСТ: Принудительная отправка уведомления пользователю {user_id}")
                    
                    # Создаём задачу для отправки в текущем loop
                    asyncio.create_task(
                        self._send_notification(user_id, full_product)
                    )
                    
                    # Ждём немного, чтобы задача успела начаться
                    await asyncio.sleep(0.1)
                    
                    # ПРОДАКШЕН КОД:
                    # if result.get("is_changed", False):
                    #     logger.info(f"🔔 Цена изменилась для товара {product_id}")
                    #     asyncio.create_task(
                    #         self._send_notification(user_id, full_product)
                    #     )
                    #     await asyncio.sleep(0.1)
                    
                    logger.info("🧪 ТЕСТ: Остановка после первого товара")
                    break
                        
                except Exception as e:
                    logger.error(f"Ошибка при обработке товара: {e}", exc_info=True)
                    continue

            logger.info("✅ Автоматическое обновление цен завершено.")

        except Exception as e:
            logger.error(f"Ошибка при выполнении планового обновления: {e}", exc_info=True)

    async def _send_notification(self, chat_id: str, full_product: dict):
        """Отправка уведомления."""
        try:
            logger.info(f"📤 Попытка отправки уведомления пользователю {chat_id}")
            
            # Формируем текст напрямую здесь
            text = f"🔔 Цена на товар изменилась!\n\n" \
                   f"📦 {full_product['name']}\n\n" \
                   f"💰 Старая цена: {full_product['latest_price']['previous_price_with_card']} ₽\n" \
                   f"💰 Новая цена: {full_product['latest_price']['with_card']} ₽\n\n" \
                   f"🔗 {full_product['link']}"
            
            logger.info(f"📝 Текст сформирован: {text[:50]}...")
            
            # Прямая отправка через бота
            message = await self.bot.send_message(
                chat_id=int(chat_id),
                text=text
            )
            
            logger.info(f"✅ Сообщение ID {message.message_id} отправлено пользователю {chat_id}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке уведомления пользователю {chat_id}: {e}", exc_info=True)
