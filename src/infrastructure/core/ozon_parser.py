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
    """
    Класс для парсинга данных с сайта Ozon.

    Использует SessionEngine для управления WebDriver и selenium-stealth для обхода
    анти-бот систем. Основной метод parse_product извлекает все данные товара в одной сессии.

    Пример использования:
        parser = OzonParser()
        data = parser.parse_product("https://www.ozon.ru/product/123456789")
        print(f"Название товара: {data['name']}")
        print(f"Артикул: {data['id']}")
        print(f"Рейтинг: {data['rating']}")
    """

   # Способ 2: Проверка через Selenium (косвенно)
    @session_wrapper(headless=True)
    def get_page_status(self, session: SessionEngine, url: str) -> bool:
        """
        Проверка доступности страницы через Selenium.
        
        Args:
            session: Экземпляр SessionEngine
            url: URL для проверки
            
        Returns:
            bool: True если страница загрузилась корректно, False иначе
        """
        try:
            session.navigate(url)
            
            # Проверяем наличие специфичных элементов Ozon или отсутствие страниц ошибок
            wait = WebDriverWait(session.driver, 5)
            
            # Проверяем на 404 страницу
            if "404" in session.driver.title.lower() or "не найден" in session.driver.title.lower():
                return False
                
            # Проверяем на блокировку/капчу
            if "blocked" in session.driver.page_source.lower() or "captcha" in session.driver.page_source.lower():
                return False
                
            # Проверяем что это действительно страница товара Ozon
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-widget='webProductHeading']")))
                return True
            except TimeoutException:
                # Если основной элемент не найден, проверяем другие признаки
                if "ozon.ru" in session.driver.current_url and len(session.driver.page_source) > 1000:
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Ошибка при проверке страницы {url}: {e}")
            return False


    @session_wrapper(headless=True)
    def parse_product(self, session: SessionEngine, url: str) -> Dict:
        """
        Извлекает все данные о товаре с указанной страницы на Ozon в одной сессии.

        Args:
            session (SessionEngine): Экземпляр движка сессии с настроенным WebDriver.
            url (str): URL страницы товара.

        Returns:
            Dict: Словарь с данными товара (name, id, rating, price_with_card, price_without_card,
                  price_default, image_url, categories).
        """
        try:
            session.navigate(url)
            logger.info(f"Загружена страница: {url}")
            return {
                "name": self._extract_name(session),
                "id": self._extract_id(session),
                "rating": self._extract_rating(session),
                "price_with_card": self._extract_price_with_card(session),
                "price_without_card": self._extract_price_without_card(session),
                "price_default": self._extract_price_default(session),
                "image_url": self._extract_image_url(session),
                "categories": self._extract_category_product(session)
            }
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            return {
                "name": "N/A",
                "id": "N/A",
                "rating": 0.0,
                "price_with_card": 0,
                "price_without_card": 0,
                "price_default": 0,
                "image_url": "N/A",
                "categories": []
            }

    def _extract_name(self, session: SessionEngine) -> str:
        """
        Извлекает название товара.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            str: Название товара или "N/A" в случае ошибки.
        """
        try:
            name_element = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = session._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"

    def _extract_id(self, session: SessionEngine) -> str:
        """
        Извлекает артикул товара.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            str: Артикул товара или "N/A" в случае ошибки.
        """
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
            return "N/A"
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"

    def _extract_rating(self, session: SessionEngine) -> float:
        """
        Извлекает рейтинг товара.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            float: Рейтинг товара (например, 4.5) или 0.0 в случае ошибки.
        """
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
            return 0.0

    def _extract_price_with_card(self, session: SessionEngine) -> int:
        """
        Извлекает цену с картой.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            int: Цена с картой (в рублях) или 0 в случае ошибки.
        """
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
            return 0

    def _extract_price_without_card(self, session: SessionEngine) -> int:
        """
        Извлекает цену без карты.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            int: Цена без карты (в рублях) или 0 в случае ошибки.
        """
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
            return 0

    def _extract_price_default(self, session: SessionEngine) -> int:
        """
        Извлекает базовую цену.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            int: Базовая цена (в рублях) или 0 в случае ошибки.
        """
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
            return 0

    def _extract_image_url(self, session: SessionEngine) -> str:
        """
        Извлекает URL изображения товара.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            str: URL изображения или "N/A" в случае ошибки.
        """
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
            return "N/A"

    def _extract_category_product(self, session: SessionEngine) -> List[str]:
        """
        Извлекает категории товара из списка ol/li.

        Args:
            session (SessionEngine): Экземпляр движка сессии.

        Returns:
            List[str]: Список категорий или пустой список в случае ошибки.
        """
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
            return []

    def _parse_rating(self, text: str) -> float:
        """
        Вспомогательный метод для извлечения рейтинга из текста.

        Args:
            text (str): Текст, содержащий рейтинг (например, "4.9 • 5 058 отзывов").

        Returns:
            float: Числовое значение рейтинга или 0.0, если преобразование не удалось.
        """
        if not text or text == "N/A":
            return 0.0
        try:
            # Извлекаем число до "•" (например, "4.9" из "4.9 • 5 058 отзывов")
            return float(text.split("•")[0].replace(",", ".").strip())
        except (ValueError, AttributeError, IndexError):
            logger.error(f"Не удалось преобразовать текст рейтинга: {text}")
            return 0.0

    def _parse_number(self, text: str) -> int:
        """
        Вспомогательный метод для извлечения числа из текста (удаление '₽' и пробелов).

        Args:
            text (str): Текст, содержащий цену (например, "1 234 ₽").

        Returns:
            int: Числовое значение цены или 0, если преобразование не удалось.
        """
        if not text or text == "N/A":
            return 0
        try:
            cleaned_text = "".join(filter(str.isdigit, text))
            return int(cleaned_text) if cleaned_text else 0
        except (ValueError, AttributeError):
            logger.error(f"Не удалось преобразовать текст цены: {text}")
            return 0

# Пример вызова
if __name__ == "__main__":
    parser = OzonParser()
    ozon_url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"
    product_data = parser.parse_product(ozon_url)
    status_code = parser.get_page_status(ozon_url)
    print(f"Название товара: {product_data['name']}")
    print(f"ID товара: {product_data['id']}")
    print(f"Рейтинг товара: {product_data['rating']}")
    print(f"Цена товара с картой: {product_data['price_with_card']}")
    print(f"Цена товара без карты: {product_data['price_without_card']}")
    print(f"Цена товара дефолт: {product_data['price_default']}")
    print(f"Изображение товара: {product_data['image_url']}")
    print(f"Категории товара: {product_data['categories']}")
    print(f'СТАТУС HTTP -> {status_code}')