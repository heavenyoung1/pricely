import schedule
import time

from src.application.interfaces.repositories import ProductRepository, PriceRepository
from src.infrastructure.parsers import OzonParser
from src.application.use_cases import CompareProductPriceUseCase
from src.infrastructure.notifications import NotificationService


class JobScheduler:
    """Класс для планирования задач, запускающий парсер по расписанию."""

    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository, parser: OzonParser, notification_service: NotificationService):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.parser = parser
        self.notification_service = notification_service

    def schedule_price_check(self):
        """Планирует выполнение проверки цен каждые 1 час."""
        def job():
            use_case = CompareProductPriceUseCase(self.product_repo, self.price_repo, self.parser, self.notification_service)
            products = self.product_repo.get_all("some_user_id")  # Получить всех пользователей
            for product in products:
                use_case.execute(product.id)

        schedule.every(1).hours.do(job)

        # Запускаем цикл для выполнения задачи
        while True:
            schedule.run_pending()
            time.sleep(60)
