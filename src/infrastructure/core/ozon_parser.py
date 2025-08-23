from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .session_decorator import session_engine_decorator as session_wrapper
from .session_engine import SessionEngine
import logging
import sys
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ozon_parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class OzonParser:

    @session_wrapper(headless=True)
    def execute_name(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            name_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = session._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"
        
    @session_wrapper(headless=True)
    def execute_ID(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            elements = WebDriverWait(session.driver, session.wait_time).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            
            # Ищем элемент с текстом "Артикул:"
            for element in elements:
                text = element.text.strip() if element else "N/A"
                if "Артикул:" in text:
                    articule = text.replace("Артикул:", "").strip()
                    logger.info(f"Найден артикул: {articule}")
                    return articule
            
            logger.warning("Элемент с 'Артикул:' не найден")
            return "N/A"
            
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"
        
    @session_wrapper(headless=True)
    def execute_rating(self, session: SessionEngine, url: str) -> float:
        try:
            session.navigate(url)
            rating_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gaP12835-a2') and contains(@class, 'tsBodyControl500Medium')]"))
            )
            rating_text = session._extract_text(rating_element)
            logger.info(f'RAITING TEXT {rating_text}')
            rating = self._extract_rating(rating_text)
            logger.info(f"Найден рейтинг: {rating}")
            return rating
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            return 0.0
        
    @session_wrapper(headless=True)
    def execute_price_with_card(self, session: SessionEngine, url: str) -> int:

        try:
            session.navigate(url)
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'tsHeadline600Large')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return 0

    @session_wrapper(headless=True)
    def execute_price_without_card(self, session: SessionEngine, url: str) -> int:

        try:
            session.navigate(url)
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'pdp_bf1')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return 0
        
    @session_wrapper(headless=True)
    def execute_price_default(self, session: SessionEngine, url: str) -> int:
        try:
            session.navigate(url)
            price_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'pdp_f0b') and contains(@class, 'pdp_b1f') and contains(@class, 'pdp_bf0')]"))
            )
            price_text = session._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена базовая цена: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении базовой цены: {e}")
            return 0
        
    @session_wrapper(headless=True)
    def execute_image_url(self, session: SessionEngine, url: str) -> str:
        try:
            session.navigate(url)
            image_container = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'pdp_v3 pdp_v4')]"))
            )
            image_url = self._extract_image_url(image_container)
            logger.info(f"Найден URL изображения: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Ошибка при извлечении URL изображения: {e}")
            return "N/A"

    @session_wrapper(headless=True)
    def execute_category_product(self, session: SessionEngine, url: str) -> List[str]:
        try:
            session.navigate(url)
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
            return []






    def _extract_text(self, element) -> str:
        """Вспомогательный метод для извлечения текста элемента."""
        try:
            return element.text.strip() if element else "N/A"
        except:
            return "N/A"
        
    def _extract_rating(self, text: str) -> float:
        """Вспомогательный метод для извлечения рейтинга из текста."""
        if not text or text == "N/A":
            return 0.0
        # Извлекаем число до "•" (например, "4.9" из "4.9 • 5 058 отзывов")
        return float(text.split("•")[0].strip()) if "•" in text else 0.0
    
    def _extract_number(self, text: str) -> int:
        """Вспомогательный метод для извлечения числа из текста (удаление '₽' и пробелов)."""
        if not text or text == "N/A":
            return 0
        return int("".join(filter(str.isdigit, text)))


# Пример вызова
if __name__ == "__main__":
    parser = OzonParser()
    ozon_url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"
    product_name = parser.execute_name(ozon_url)
    product_id = parser.execute_ID(ozon_url)
    product_score = parser.execute_rating(ozon_url)
    with_card = parser.execute_price_with_card(ozon_url)
    without_card = parser.execute_price_without_card(ozon_url)
    default = parser.execute_price_default(ozon_url)
    image_url = parser.execute_image_url(ozon_url)    
    cate = parser.execute_category_product(ozon_url)    
    print(f"Название товара: {product_name}")
    print(f"ID товара: {product_id}")
    print(f"Рейтинг товара: {product_score}")
    print(f"Цена товара с картой: {with_card}")
    print(f"Цена товара без карты: {without_card}")
    print(f"Цена товара дефолт: {default}")
    print(f"Изображение товара: {image_url}")
    print(f"Категории товара: {cate}")




































