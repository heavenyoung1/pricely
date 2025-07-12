from domain.repositories.product_repository import ProductRepository
from adapters.session_engine import SessionEngine
from adapters.selenium_adapter import SeleniumAdapter
from domain.entities.product import Product
from utils.state_manager import StateManager
from utils.logger import logger
import schedule
import time
import requests

from config.settings import bot_token, chat_id

class PriceTrackerUseCase:
    def __init__(self, repository: ProductRepository, state_manager: StateManager, urls: list, chat_id: str, bot_token: str):
        self.repository = repository
        self.state_manager = state_manager
        self.urls = urls                    # Список URL для мониторинга
        self.chat_id = chat_id              # ID чата Telegram
        self.bot_token = bot_token          # Токен бота Telegram

    def check_price_change(self, url: str):
        '''Проверяет изменение цены для заданного URL'''
        try:
            logger.info(f'Проверка цены для URL: {url}')
            product = self.repository.get_product_data(url)
            previous_price = self.state_manager.get_previous_price(url)
            current_price = product.price_without_card

            if previous_price > 0 and current_price != previous_price:
                price_change = current_price - previous_price
                message = (f'Цена изменена для {product.name}!\n'
                           f'URL: {url}\n'
                           f'Предыдущая цена: {previous_price} руб.\n'
                           f'Текущая цена: {current_price} руб.\n'
                           f'Изменение: {price_change} руб.')
                self._send_telegram_message(message)
                logger.info(f'Отправлено уведомление об изменении цены: {message}')
            else:
                logger.info(f'Цена для {url} не изменилась или это первая проверка')

            # Обновляем сохраненную цену
            self.state_manager.update_price(url, current_price)
            product.previous_price_without_card = previous_price # Обновляем для следующей итерации

        except Exception as e:
            logger.error(f'Ошибка при проверке цены для {url}: {e}')

    def _send_telegram_message(self, message: str):
        '''Отправляет сообщение в Telegram'''
        url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'
        payload = {
            'chat_id': self.chat_id,
            'text': message
        }
        try:
            response = requests.post(url=url, data=payload)
            if response.status_code == 200:
                logger.info(f'Сообщение успешно отправлено в Telegram')
            else:
                logger.error(f'Ошибка отправки сообщения в Telegram: {response.text}')
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в Telegram: {e}')

    def start_tracking(self, interval_hours: int = 1):
        '''Запуск периодической проверки цен'''
        logger.info('Запуск отслеживания цен с интервалом {interval_hours} часов')
        for url in self.urls:
            schedule.every(interval_hours).hours.do(self.check_price_change, url)

        while True:
            schedule.run_pending()
            time.sleep(60) # Проверка каждую минуту

# Тестирование
if __name__ == "__main__":
    session = SessionEngine(headless=True)
    selenium_adapter = SeleniumAdapter(session)
    state_manager = StateManager()
    urls = ['https://www.ozon.ru/product/shorty-meet-aida-belyy-1550627699/']
    chat_id = chat_id
    bot_token = bot_token
    tracker = PriceTrackerUseCase(selenium_adapter, state_manager, urls, chat_id, bot_token)
    tracker.start_tracking(1)  # Проверка каждый час