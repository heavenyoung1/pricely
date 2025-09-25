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

    @staticmethod
    def _extract_digits(text: str) -> int:
        """Возвращает только цифры из строки"""
        return int("".join(ch for ch in text if ch.isdigit()))

    @session_wrapper(headless=True)
    def extract_articule(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Артикул')]"))
            )
            element_text = session._extract_text(element_obj)
            logger.info(f"Найдена информация о товаре: {element_text}")
            # Разбить данные и убрать знак рубля
            return self._extract_digits(element_text)
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None

    @session_wrapper(headless=True)
    def extract_name(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            element_text = session._extract_text(element_obj)
            logger.info(f"Найдена информация о товаре: {element_text}")
            return element_text
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None
        
    @session_wrapper(headless=True)
    def extract_price_with_card(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@class='tsHeadline600Large']"))
            )
            element_text = session._extract_text(element_obj)
            logger.info(f"Найдена информация о товаре: {element_text}")
            # Разбить данные и убрать знак рубля
            return self._extract_digits(element_text)
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None
        
    @session_wrapper(headless=True)
    def extract_price_without_card(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'₽') and contains(@class,'tsHeadline500Medium')]"))
            )
            element_text = session._extract_text(element_obj)
            logger.info(f"Найдена информация о товаре: {element_text}")
            # Разбить данные и убрать знак рубля
            return self._extract_digits(element_text)
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None
        
            
    @session_wrapper(headless=True)
    def extract_categories(self, session: SessionEngine, url: str) -> List[str]:
        try:
            session.navigate(url)
            elements = WebDriverWait(session.driver, session.wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ol//li//span"))
            )
            categories = [session._extract_text(e).strip() for e in elements if session._extract_text(e)]
            logger.info(f"Категории: {categories}")
            return categories
        except Exception as e:
            logger.error(f'Ошибка при извлечении категорий: {e}')
            return []
    
    @session_wrapper(headless=True)
    def extract_raiting(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            #Здесь берется только первый обект, остальные не берутся в результат , нужно поправить
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'отзыв')]"))
            )
            element_text = session._extract_text(element_obj) # например: "4.8 • 233 отзыва"
            rating_part, reviews_part = element_text.split("•")
            rating = float(rating_part.strip().replace(",", "."))
            logger.info(f"Найдена информация о товаре: {element_text}")
            # Разбить данные и убрать знак рубля
            return rating
        except Exception as e:
            logger.error(f'Ошибка при извлечении названия товара: {e}')
            return None
        
    @session_wrapper(headless=True)
    def extract_image(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-widget='webGallery']//img"))
            )
            image_url = element_obj.get_attribute("src")
            if image_url:
                # увеличиваем качество до 1000px
                image_url = image_url.replace("/wc38/", "/wc1000/").replace("/wc50/", "/wc1000/")
            logger.info(f"Найдено изображение: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f'Ошибка при извлечении изображения: {e}')
            return None

if __name__ == "__main__":
    parser = OzonParser()
    # result = parser.extract_name('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    # result_1 = parser.extract_price_with_card('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    # result_2 = parser.extract_price_without_card('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    # result_3 = parser.extract_articule('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    result_4 = parser.extract_categories('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    # result_5 = parser.extract_raiting('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    result_6 = parser.extract_image('https://www.ozon.ru/product/aroma-stikery-dlya-obuvi-30-sht-dezodorant-dlya-obuvi-antibakterialnyy-1723889987/?at=DqtDqnm7Nup54QYmswEpQYXFpp2VXvSM0rqokI66QJ32')
    # print(result)
    # print(result_1)
    # print(result_2)
    # print(result_3)
    print(result_4)
    # print(result_5)
    print(result_6)