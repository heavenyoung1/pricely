from domain.entities.product import Product
from adapters.session_engine import SessionEngine
from utils.logger import logger


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class OzonParserUseCase:
    def __init__(self, session_engine: SessionEngine, url: str):
        self.session = session_engine
        self.base_url = "https://www.ozon.ru/"
        self.url = url

    # def execute_name_of_product(self) -> str:
    #         """Извлекает название товара с указанной страницы."""
    #         try:
    #             self.session.navigate(self.url)  # Исправлен вызов метода
    #             # Используем XPath для поиска названия
    #             name_element = self.session.find_element(by="xpath", value="//div[@data-widget='webProductHeading']//h1")
    #             name = name_element.text if name_element else "N/A"
    #             logger.info(f"Найдено название товара: {name}")
    #             return name
    #         except Exception as e:
    #             logger.error(f"Ошибка при извлечении названия товара: {e}")
    #             return "N/A"

    def execute_name(self) -> str:
        """Извлекает название товара с указанной страницы"""
        try:
            self.session.navigate(self.url)
            # Ждем, пока элемент станет видимым (до 10 секунд)
            name_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
            )
            name = name_element.text if name_element else "N/A"
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return "N/A"
    
    def execute_articule_ID(self) -> str:
        """Извлекает название артикул (ID) с указанной страницы"""
        try:
            self.session.navigate(self.url)
            # Ждем, пока элемент с артикулом станет видимым
            articule_element = WebDriverWait(self.session.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ga5_3_1-a2') and contains(@class, 'tsBodyControl400Small')]"))
            )
            # Извлекаем текст и убираем префикс "Артикул: "
            articule_text = articule_element.text.strip()
            articule = articule_text.replace("Артикул: ", "").strip() if articule_text else "N/A"
            logger.info(f"Найден артикул: {articule}")
            return articule
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return "N/A"


# Тестирование функции
if __name__ == "__main__":
    # Создаем экземпляр SessionEngine
    session = SessionEngine(headless=True)
    # Создаем экземпляр OzonParserUseCase с session и url
    ozon = OzonParserUseCase(session, 'https://www.ozon.ru/product/shorty-meet-aida-belyy-1550627699/')
    # Вызываем метод
    name = ozon.execute_name()
    articule = ozon.execute_articule_ID()
    print(f"Название товара: {name}")
    print(f"Артикул: {articule}")

    # Закрываем сессию
    session.close()