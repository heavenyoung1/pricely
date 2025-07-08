from domain.entities.product import Product
from adapters.session_engine import SessionEngine
from utils.logger import logger

class OzonParserUseCase:
    def __init__(self, session_engine: SessionEngine, url: str):
        self.session = session_engine
        self.base_url = "https://www.ozon.ru/"
        self.url = url

    def execute_name_of_product(self):
        self.session.navigate(self, self.url)
        name = self.session.

    def execute(self) -> list[Product]:
        """Выполняет парсинг товаров с Ozon с использованием XPath"""
