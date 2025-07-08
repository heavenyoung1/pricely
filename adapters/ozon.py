from domain.entities.product import Product
from adapters.session_engine import SessionEngine
from utils.logger import logger


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import List

class OzonParserUseCase:
    def __init__(self, session_engine: SessionEngine, url: str):
        self.session = session_engine
        self.url = url

    def _extract_text(self, element) -> str:
        """Вспомогательный метод для извлечения текста элемента."""
        return element.text.strip() if element else ""

    def _extract_number(self, text: str) -> int:
        """Вспомогательный метод для извлечения числа из текста (удаление '₽' и пробелов)."""
        if not text or text == "N/A":
            return 0
        return int("".join(filter(str.isdigit, text)))

    def _extract_rating(self, text: str) -> float:
        """Вспомогательный метод для извлечения рейтинга из текста."""
        if not text or text == "N/A":
            return 0.0
        # Извлекаем число до "•" (например, "4.9" из "4.9 • 5 058 отзывов")
        return float(text.split("•")[0].strip()) if "•" in text else 0.0

    def _extract_discount_amount(self, price_with_card: int, price_without_card: int) -> float:
        """Вычисляет сумму скидки на основе цен с и без карты."""
        if price_without_card > 0 and price_with_card > 0:
            return price_without_card - price_with_card
        return 0.0

    def _extract_image_url(self, element) -> str:
        """Извлекает URL изображения из элемента <img>."""
        if element and element.find_element(by="tag name", value="img"):
            img_element = element.find_element(by="tag name", value="img")
            return img_element.get_attribute("src") or "N/A"
        return "N/A"

    def execute_articule(self) -> str:
        """Извлекает артикул с указанной страницы."""
        try:
            self.session.navigate(self.url)
            articule_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            articule_text = self._extract_text(articule_element)
            articule = articule_text.replace("Артикул: ", "").strip() if articule_text else "N/A"
            logger.info(f"Найден артикул: {articule}")
            return articule
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"

    def execute_name_of_product(self) -> str:
        """Извлекает название товара с указанной страницы."""
        try:
            self.session.navigate(self.url)
            name_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = self._extract_text(name_element)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"

    def execute_rating(self) -> float:
        """Извлекает рейтинг товара с указанной страницы."""
        try:
            self.session.navigate(self.url)
            rating_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl500Medium')]"))
            )
            rating_text = self._extract_text(rating_element)
            rating = self._extract_rating(rating_text)
            logger.info(f"Найден рейтинг: {rating}")
            return rating
        except Exception as e:
            logger.error(f"Ошибка при извлечении рейтинга: {e}")
            return 0.0

    def execute_price_with_card(self) -> int:
        """Извлекает цену с картой с указанной страницы."""
        try:
            self.session.navigate(self.url)
            price_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'ky3_27') and contains(@class, 'k1y_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return 0

    def execute_price_without_card(self) -> int:
        """Извлекает цену без карты с указанной страницы."""
        try:
            self.session.navigate(self.url)
            price_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'y7k_27') and contains(@class, 'ky8_27') and contains(@class, 'k1z_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return 0

    def execute_price_default(self) -> int:
        """Извлекает базовую цену с указанной страницы."""
        try:
            self.session.navigate(self.url)
            price_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'k7y_27') and contains(@class, 'k8y_27') and contains(@class, 'k6y_27') and contains(@class, 'yk7_27')]"))
            )
            price_text = self._extract_text(price_element)
            price = self._extract_number(price_text)
            logger.info(f"Найдена базовая цена: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении базовой цены: {e}")
            return 0

    def execute_image_url(self) -> str:
        """Извлекает URL изображения товара с указанной страницы."""
        try:
            self.session.navigate(self.url)
            image_container = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'jk2_27') and contains(@class, 'j2k_27')]"))
            )
            image_url = self._extract_image_url(image_container)
            logger.info(f"Найден URL изображения: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Ошибка при извлечении URL изображения: {e}")
            return "N/A"

    def execute_category_product(self) -> List[str]:
        """Извлекает категории товара с указанной страницы."""
        try:
            self.session.navigate(self.url)
            # Предположим, что категории находятся в элементах с классом (нужен реальный XPath)
            category_elements = self.session.find_elements(by="xpath", value="//div[contains(@class, 'breadcrumbs')]//a")
            categories = [self._extract_text(elem) for elem in category_elements if self._extract_text(elem)]
            logger.info(f"Найдены категории: {categories}")
            return categories if categories else []
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            return []