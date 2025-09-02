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

    @session_wrapper
    @staticmethod
    def get_http(self, session: SessionEngine, url: str):
        session.navigate(url)
        r = requests.get(url)
        print(r.status_code)

    @session_wrapper(headless=True)
    def parse_product(self, session: SessionEngine, url: str) -> Dict:
        try:
            session.navigate(url)
            logger.info(f"Загружена страница: {url}")
            return {
                "id": self._extract_id(session),
                "name": self._extract_name(session),
                "rating": self._extract_rating(session),
                "price_with_card": self._extract_price_with_card(session),
                "price_without_card": self._extract_price_without_card(session),
                "price_default": self._extract_price_default(session),
                "image_url": self._extract_image_url(session),
                "categories": self._extract_category_product(session)
            }
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            raise
    def _extract_name(self, session: SessionEngine) -> str:
        try:
            name_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = session._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return None

    def _extract_id(self, session: SessionEngine) -> str:
        try:
            elements = WebDriverWait(session.driver, session.wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            for element in elements:
                text = session._extract_text(element)
                if "Артикул:" in text:
                    articule = text.replace("Артикул:", "").strip()
                    logger.info(f"Найден артикул: {articule}")
                    return articule
            logger.warning("Элемент с 'Артикул:' не найден")
            return None
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            raise

    def _extract_rating(self, session: SessionEngine) -> float:
        try:
            rating_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gaP12835-a2') and contains(@class, 'tsBodyControl500Medium')]"))
            )
            rating_text = session._extract_text(rating_element)
            logger.info(f"Текст рейтинга: {rating_text}")
            rating = self._parse_rating(rating_text)
            logger.info(f"Найден рейтинг: {rating}")
            return rating
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            raise

    def _extract_price_with_card(self, session: SessionEngine) -> int:
        try:
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'tsHeadline600Large')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._parse_number(price_text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            raise

    def _extract_price_without_card(self, session: SessionEngine) -> int:
        try:
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'pdp_bf1')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._parse_number(price_text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            raise

    def _extract_price_default(self, session: SessionEngine) -> int:
        try:
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'pdp_f0b') and contains(@class, 'pdp_b1f') and contains(@class, 'pdp_bf0')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._parse_number(price_text)
            logger.info(f"Найдена базовая цена: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении базовой цены: {e}")
            raise

    def _extract_image_url(self, session: SessionEngine) -> str:
        try:
            image_container = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'pdp_v3 pdp_v4')]"))
            )
            img_element = image_container.find_element(By.XPATH, ".//img")
            image_url = img_element.get_attribute("src")
            logger.info(f"Найден URL изображения: {image_url}")
            return image_url if image_url else "N/A"
        except Exception as e:
            logger.error(f"Ошибка при извлечении URL изображения: {e}")
            raise

    def _extract_category_product(self, session: SessionEngine) -> List[str]:
        try:
            ol_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//ol[contains(@class, 'df9_11') and contains(@class, 'tsBodyControl400Small')]"))
            )
            category_elements = ol_element.find_elements(By.XPATH, ".//li")
            categories = []
            for elem in category_elements:
                span_element = elem.find_element(By.XPATH, ".//span")
                category_text = session._extract_text(span_element)
                if category_text:
                    categories.append(category_text)
            logger.info(f"Найдены категории: {categories}")
            return categories if categories else []
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            raise

    def _parse_rating(self, text: str) -> float:
        if not text or text == "N/A":
            return 0.0
        try:
            # Извлекаем число до "•" (например, "4.9" из "4.9 • 5 058 отзывов")
            return float(text.split("•")[0].replace(",", ".").strip())
        except (ValueError, AttributeError, IndexError):
            logger.error(f"Не удалось преобразовать текст рейтинга: {text}")
            raise

    def _parse_number(self, text: str) -> int:
        if not text or text == "N/A":
            return 0
        try:
            cleaned_text = "".join(filter(str.isdigit, text))
            return int(cleaned_text) if cleaned_text else 0
        except (ValueError, AttributeError):
            logger.error(f"Не удалось преобразовать текст цены: {text}")
            raise

OzonParser.get_http('https://www.ozon.ru/product/dzhinsy-befree-883110146/')