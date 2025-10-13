from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .session_decorator import session_engine_decorator as session_wrapper
from .session_engine import SessionEngine
from typing import Dict, List
import logging
import sys
import requests
from selenium.common.exceptions import WebDriverException, TimeoutException
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

    @session_wrapper(headless=False)
    def parse_product(self, session: SessionEngine, url: str) -> Dict:
        try:
            session.navigate(url)
            logger.info(f"Загружена страница: {url}")
            parsed_data = {
                'id': self._extract_id(session),
                'name': self._extract_name(session),
                'rating': self._extract_rating(session),
                'price_with_card': self._extract_price_with_card(session),
                'price_without_card': self._extract_price_without_card(session),
                'image_url': self._extract_image_url(session),
                'categories': self._extract_categories(session)
            }
            logger.info(f"Данные, полученные парсером: {parsed_data}")
            return parsed_data
        except Exception as e:
            logger.error(f'Ошибка при парсинге страницы {url}: {e}')
            raise

    # ----------------- Вспомогательные методы -----------------

    def _extract_digits(self, text: str) -> int:
        """Возвращает только цифры из строки"""
        return int("".join(ch for ch in text if ch.isdigit()))

    def _extract_id(self, session: SessionEngine) -> str:
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Артикул')]"))
            )
            text = session._extract_text(element_obj)
            articule = self._extract_digits(text)
            logger.info(f"Найден артикул: {articule}")
            return str(articule)
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return None

    def _extract_name(self, session: SessionEngine) -> str:
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = session._extract_text(element_obj)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return None

    def _extract_price_with_card(self, session: SessionEngine) -> int:
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[@class='tsHeadline600Large']"))
            )
            text = session._extract_text(element_obj)
            price = self._extract_digits(text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return None

    def _extract_price_without_card(self, session: SessionEngine) -> int:
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'₽') and contains(@class,'tsHeadline500Medium')]"))
            )
            text = session._extract_text(element_obj)
            price = self._extract_digits(text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return None

    def _extract_categories(self, session: SessionEngine) -> List[str]:
        try:
            elements = WebDriverWait(session.driver, session.wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ol//li//span"))
            )
            categories = [session._extract_text(e).strip() for e in elements if session._extract_text(e)]
            logger.info(f"Найдены категории: {categories}")
            return categories
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            return []

    def _extract_rating(self, session: SessionEngine) -> float:
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'отзыв')]"))
            )
            text = session._extract_text(element_obj)  # например: "4.8 • 233 отзыва"
            rating_part, _ = text.split("•")
            rating = float(rating_part.strip().replace(",", "."))
            logger.info(f"Найден рейтинг: {rating}")
            return rating
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            return None

    def _extract_image_url(self, session: SessionEngine) -> str:
        try:
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
            logger.error(f"Ошибка при извлечении изображения: {e}")
            return None