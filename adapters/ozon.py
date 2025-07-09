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
        self.wait = WebDriverWait(self.session.driver, 10)

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
    
    def _calculate_discount(self, price_now, price_old) -> int:
        """Вычисляет сумму скидки на основе цен с и без карты."""
        price_now = self.execute_price_without_card()
        price_old = self.execute_price_default()
        discount = int(((price_old - price_now) / price_old) * 100) // 1
        logger.info(f"Размер скидки составляет: {discount}%")
        return discount

    def _extract_image_url(self, element) -> str:
        """Извлекает URL изображения из элемента <img>."""
        if element and element.find_element(by="tag name", value="img"):
            img_element = element.find_element(by="tag name", value="img")
            return img_element.get_attribute("src") or "N/A"
        return "N/A"

    def execute_articule(self) -> str:
        """Извлекает артикул с указанной страницы, проверяя наличие текста 'Артикул:'."""
        try:
            elements = WebDriverWait(self.session.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
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

    def execute_name_of_product(self) -> str:
        """Извлекает название товара с указанной страницы."""
        try:
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
        """Извлекает категории товара с указанной страницы из списка ol/li."""
        try:
            # Ждем, пока список ol станет видимым
            ol_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//ol[contains(@class, 'e0d_11') and contains(@class, 'tsBodyControl400Small')]"))
            )
            # Находим все li внутри ol
            category_elements = ol_element.find_elements(by="xpath", value=".//li")
            categories = []
            for elem in category_elements:
                # Извлекаем текст из <span> внутри <a>
                span_element = elem.find_element(by="xpath", value=".//span")
                category_text = self._extract_text(span_element)
                if category_text:
                    categories.append(category_text)
            logger.info(f"Найдены категории: {categories}")
            return categories if categories else []
        except Exception as e:
            logger.error(f"Ошибка при извлечении категорий: {e}")
            return []
        
    def execute(self) -> Product:
            """Выполняет полный парсинг товара с указанной страницы."""
            try:
                self.session.navigate(self.url)
                id = self.execute_articule()
                name = self.execute_name_of_product()
                rating = self.execute_rating()
                price_with_card = self.execute_price_with_card()
                price_without_card = self.execute_price_without_card()
                price_default = self.execute_price_default()
                discount_amount = self._calculate_discount(price_without_card, price_default)
                link = self.url
                url_image = self.execute_image_url()
                category_product = self.execute_category_product()

                product = Product(
                    id=id,
                    name=name,
                    rating=rating,
                    price_with_card=price_with_card,
                    price_without_card=price_without_card,
                    price_default=price_default,
                    discount_amount=discount_amount,
                    link=link,
                    url_image=url_image,
                    category_product=category_product
                )
                logger.info(f"Успешно создан объект Product: {product}")
                return product
            except Exception as e:
                logger.error(f"Ошибка при полном парсинге: {e}")
                return Product("N/A", "N/A", 0.0, 0, 0, 0, 0.0, self.url, "N/A", [])

# Тестирование функции
if __name__ == "__main__":
    # Создаем экземпляр SessionEngine
    session = SessionEngine(headless=True)
    # Создаем экземпляр OzonParserUseCase с session и url
    ozon = OzonParserUseCase(session, 'https://www.ozon.ru/product/shorty-meet-aida-belyy-1550627699/')
    # Вызываем метод
    product = ozon.execute()
    print(f"Получен продукт: {product}")

    # Закрываем сессию
    session.close()