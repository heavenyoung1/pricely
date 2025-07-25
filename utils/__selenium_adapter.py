from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List

from adapters.session_engine import SessionEngine
from domain.entities.product import Product
from utils.logger import logger

class SeleniumAdapter:
    def __init__(self, session_engine: SessionEngine):
        self.session = session_engine
        self.waiting_driver = WebDriverWait(self.session.driver, 10)  # Единый объект для ожидания

    def get_product_data(self, url: str) -> Product:
        """Извлекает все данные продукта с указанной страницы."""
        try:
            logger.info(f"Начинаем навигацию на URL: {url}")
            self.session.navigate(url)
            logger.info(f"Успешно перешли на URL: {url}")
            product = Product(
                id=self.get_articule(),
                name=self.get_name(),
                rating=self.get_rating(),
                price_with_card=self.get_price_with_card(),
                price_without_card=self.get_price_without_card(),
                previous_price_without_card=0, # Значение по умолчанию, обновляется в use case
                price_default=self.get_price_default(),
                link=url,
                url_image=self.get_image_url(),
                category_product=self.get_categories()
            )
            logger.info(f"Успешно собраны данные продукта: {product}")
            return product
        except Exception as e:
            logger.error(f"Ошибка при извлечении данных продукта: {e}")
            return Product("N/A", "N/A", 0.0, 0, 0, 0, 0, 0, 0.0, url, "N/A", [])

    def _extract_text(self, element) -> str:
        """Вспомогательный метод для извлечения текста элемента."""
        text = element.text.strip() if element else ""
        logger.debug(f"Извлечен текст: {text}")
        return text

    def _extract_number(self, text: str) -> int:
        """Вспомогательный метод для извлечения числа из текста."""
        if not text or text == "N/A":
            logger.debug("Текст пустой или 'N/A', возвращаем 0")
            return 0
        number = int("".join(filter(str.isdigit, text)))
        logger.debug(f"Извлечено число: {number}")
        return number

    def _extract_rating(self, text: str) -> float:
        """Вспомогательный метод для извлечения рейтинга из текста."""
        if not text or text == "N/A":
            logger.debug("Текст пустой или 'N/A', возвращаем 0.0")
            return 0.0
        rating = float(text.split("•")[0].strip()) if "•" in text else 0.0
        logger.debug(f"Извлечен рейтинг: {rating}")
        return rating

    def _extract_image_url(self, element):
        """Извлекает URL изображения из элемента <img>."""
        if element and element.find_element(by="tag name", value="img"):
            img_element = element.find_element(by="tag name", value="img")
            url = img_element.get_attribute("src") or "N/A"
            logger.debug(f"Извлечен URL изображения: {url}")
            return url
        logger.debug("Не удалось извлечь URL изображения, возвращаем 'N/A'")
        return "N/A"

    def get_articule(self) -> str:
        """Извлекает артикул."""
        try:
            logger.info("Начинаем поиск элемента с артикулом")
            elements = self.waiting_driver.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            logger.info(f"Найдено {len(elements)} элементов для проверки артикула")
            for element in elements:
                text = self._extract_text(element)
                if "Артикул:" in text:
                    articule = text.replace("Артикул: ", "").strip()
                    logger.info(f"Найден артикул: {articule}")
                    return articule
            logger.error("Элемент с 'Артикул:' не найден")
            return "N/A"
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"

    def get_name(self) -> str:
        """Извлекает название товара."""
        try:
            logger.info("Начинаем поиск элемента с названием товара")
            name_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = self._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"

    def get_rating(self) -> float:
        """Извлекает рейтинг товара."""
        try:
            logger.info("Начинаем поиск элемента с рейтингом")
            rating_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl500Medium')]"))
            )
            rating_text = self._extract_text(rating_element)
            rating = self._extract_rating(rating_text)
            logger.info(f"Найден рейтинг: {rating}")
            return rating
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            return 0.0

    def get_price_with_card(self) -> int:
        """Извлекает цену с картой."""
        try:
            logger.info("Начинаем поиск элемента с ценой с картой")
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'ky3_27') and contains(@class, 'k1y_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return 0

    def get_price_without_card(self) -> int:
        """Извлекает цену без карты."""
        try:
            logger.info("Начинаем поиск элемента с ценой без карты")
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'y7k_27') and contains(@class, 'ky8_27') and contains(@class, 'k1z_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return 0

    def get_price_default(self) -> int:
        """Извлекает базовую цену."""
        try:
            logger.info("Начинаем поиск элемента с базовой ценой")
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'k7y_27') and contains(@class, 'k8y_27') and contains(@class, 'k6y_27') and contains(@class, 'yk7_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена базовая цена: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении базовой цены: {e}")
            return 0

    def get_image_url(self) -> str:
        """Извлекает URL изображения товара."""
        try:
            logger.info("Начинаем поиск элемента с URL изображения")
            image_container = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'jk2_27') and contains(@class, 'j2k_27')]"))
            )
            image_url = self._extract_image_url(image_container)
            logger.info(f"Найден URL изображения: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Ошибка при извлечении URL изображения: {e}")
            return "N/A"

    def get_categories(self) -> List[str]:
        """Извлекает категории товара из списка ol/li."""
        try:
            logger.info("Начинаем поиск элемента с категориями")
            ol_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//ol[contains(@class, 'e0d_11') and contains(@class, 'tsBodyControl400Small')]"))
            )
            category_elements = ol_element.find_elements(by="xpath", value=".//li")
            logger.info(f"Найдено {len(category_elements)} элементов категорий")
            categories = []
            for elem in category_elements:
                span_element = elem.find_element(by="xpath", value=".//span")
                category_text = self._extract_text(span_element)
                if category_text:
                    categories.append(category_text)
            logger.info(f"Найдены категории: {categories}")
            return categories if categories else []
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            return []
