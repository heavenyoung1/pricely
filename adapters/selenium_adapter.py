from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from adapters.session_engine import SessionEngine
from domain.entities.product import Product
from utils.logger import logger
from typing import List

class SeleniumAdapter:
    def __init__(self, session_engine: SessionEngine):
        self.session = session_engine
        self.waiting_driver = WebDriverWait(self.session.driver, 10) # Единый объект для ожидания

    def get_product_data(self, url: str) -> Product:
            """Извлекает все данные продукта с указанной страницы."""
            try:
                self.session.navigate(url)
                return Product(
                    id=self.get_articule(),
                    name=self.get_name(),
                    rating=self.get_rating(),
                    price_with_card=self.get_price_with_card(),
                    price_without_card=self.get_price_without_card(),
                    price_default=self.get_price_default(),
                    discount_amount=0.0,  # Вычисляется в use case
                    link=url,
                    url_image=self.get_image_url(),
                    category_product=self.get_categories()
                )
            except Exception as e:
                logger.error(f"Ошибка при извлечении данных продукта: {e}")
                return Product("N/A", "N/A", 0.0, 0, 0, 0, 0.0, url, "N/A", [])

    def _extract_text(self, element) -> str:
        """Вспомогательный метод для извлечения текста элемента"""
        return element.text.strip() if element else ""
        
    def _extract_number(self, text: str) -> int:
        """Вспомогательный метод для извлечения числа из текста"""
        if not text or text == 'N/A':
            return 0
        else:
            return int(''.join(filter(str.isdigit, text)))
        
    def _extract_rating(self, text: str) -> float:
        """Вспомогательный метод для извлечения рейтинга из текста"""
        if not text or text == "N/A":
            return 0.0
        return float(text.split("•")[0].strip()) if "•" in text else 0.0

    def _extract_image_url(self, element):
        """Извлекает URL изображения из элемента <img>."""
        if element and element.find_element(by="tag name", value="img"):
            img_element = element.find_element(by="tag name", value="img")
            return img_element.get_attribute("src") or "N/A"
        return "N/A"
    
    def get_articule(self) -> str:
        """Извлекает артикул"""
        try:
            elements = self.waiting_driver.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            for element in elements:
                text = self._extract_text(element)
                if "Артикул:" in text:
                    return text.replace("Артикул: ", "").strip()
            logger.error("Элемент с 'Артикул:' не найден")
            return "N/A"
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"
        
    def get_name(self) -> str:
        """Извлекает название товара."""
        try:
            name_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            return self._extract_text(name_element)
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"

    def get_rating(self) -> float:
        """Извлекает рейтинг товара."""
        try:
            rating_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl500Medium')]"))
            )
            return self._extract_rating(self._extract_text(rating_element))
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            return 0.0

    def get_price_with_card(self) -> int:
        """Извлекает цену с картой."""
        try:
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'ky3_27') and contains(@class, 'k1y_27')]"))
            )
            return self._extract_number(self._extract_text(price_element))
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return 0

    def get_price_without_card(self) -> int:
        """Извлекает цену без карты."""
        try:
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'y7k_27') and contains(@class, 'ky8_27') and contains(@class, 'k1z_27')]"))
            )
            return self._extract_number(self._extract_text(price_element))
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return 0

    def get_price_default(self) -> int:
        """Извлекает базовую цену."""
        try:
            price_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'k7y_27') and contains(@class, 'k8y_27') and contains(@class, 'k6y_27') and contains(@class, 'yk7_27')]"))
            )
            return self._extract_number(self._extract_text(price_element))
        except Exception as e:
            logger.error(f"Ошибка при извлечении базовой цены: {e}")
            return 0

    def get_image_url(self) -> str:
        """Извлекает URL изображения товара."""
        try:
            image_container = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'jk2_27') and contains(@class, 'j2k_27')]"))
            )
            return self._extract_image_url(image_container)
        except Exception as e:
            logger.error(f"Ошибка при извлечении URL изображения: {e}")
            return "N/A"

    def get_categories(self) -> List[str]:
        """Извлекает категории товара из списка ol/li."""
        try:
            ol_element = self.waiting_driver.until(
                EC.visibility_of_element_located((By.XPATH, "//ol[contains(@class, 'e0d_11') and contains(@class, 'tsBodyControl400Small')]"))
            )
            category_elements = ol_element.find_elements(by="xpath", value=".//li")
            categories = []
            for elem in category_elements:
                span_element = elem.find_element(by="xpath", value=".//span")
                category_text = self._extract_text(span_element)
                if category_text:
                    categories.append(category_text)
            return categories if categories else []
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            return []
