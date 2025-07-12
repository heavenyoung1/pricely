from domain.repositories.product_repository import ProductRepository
from adapters.session_engine import SessionEngine
from adapters.selenium_adapter import SeleniumAdapter
from domain.entities.product import Product
from utils.state_manager import StateManager
from utils.logger import logger
import schedule
import time

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
        except Exception as e:
            logger.error(f"Ошибка при проверке цены для {url}: {e}")