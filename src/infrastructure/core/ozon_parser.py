from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .session_decorator import session_engine_decorator as session_wrapper
from .session_engine import SessionEngine
import logging

logger = logging.getLogger(__name__)

class OzonParser:
    """
    Класс для парсинга данных с сайта Ozon.

    Использует SessionEngine для управления WebDriver и selenium-stealth для обхода
    анти-бот систем. Методы класса предназначены для извлечения данных с страниц товаров.

    Пример использования:
        parser = OzonParser()
        name = parser.execute_name_of_product("https://www.ozon.ru/product/123456789")
        print(f"Название товара: {name}")
    """

    @session_wrapper(headless=True)
    def execute_name_of_product(self, session: SessionEngine, url: str) -> str:
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

    # Место для добавления новых методов парсинга (например, для цены, описания и т.д.)

# Пример вызова
if __name__ == "__main__":
    parser = OzonParser()
    ozon_url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"
    product_name = parser.execute_name_of_product(ozon_url)
    print(f"Название товара: {product_name}")