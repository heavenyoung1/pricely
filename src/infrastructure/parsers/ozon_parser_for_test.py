import json
import logging
import sys
from typing import Dict, List

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .session_decorator import session_engine_decorator as session_wrapper
from .session_engine import SessionEngine
from src.infrastructure.parsers.interfaces import Parser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ozon_parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class OzonParser(Parser):
    def parse_product(self, url):
        pass

    @session_wrapper(headless=True)
    def extract_name(self, session: SessionEngine, url: str):
        try:
            session.navigate(url)
            name_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = session._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None
        
if __name__ == "__main__":
    parser = OzonParser()
    result = parser.extract_name('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    print(result)