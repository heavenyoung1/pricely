from domain.entities.product import Product
from adapters.session_engine import SessionEngine
from utils.logger import logger

class OzonParserUseCase:
    def __init__(self, session_engine: SessionEngine, url: str):
        self.session = session_engine
        self.base_url = "https://www.ozon.ru/"
        self.url = url

    def execute_name_of_product(self) -> str:
            """Извлекает название товара с указанной страницы."""
            try:
                self.session.navigate(self.url)  # Исправлен вызов метода
                # Используем XPath для поиска названия
                name_element = self.session.find_element(by="xpath", value="//div[@data-widget='webProductHeading']//h1")
                name = name_element.text if name_element else "N/A"
                logger.info(f"Найдено название товара: {name}")
                return name
            except Exception as e:
                logger.error(f"Ошибка при извлечении названия товара: {e}")
                return "N/A"


    def execute(self) -> list[Product]:
        """Выполняет парсинг товаров с Ozon с использованием XPath"""
        return None


# Тестирование функции
if __name__ == "__main__":
    # Создаем экземпляр SessionEngine
    session = SessionEngine()
    # Создаем экземпляр OzonParserUseCase с session и url
    ozon = OzonParserUseCase(session, 'https://www.ozon.ru/product/shorty-meet-aida-belyy-1550627699/')
    # Вызываем метод
    name = ozon.execute_name_of_product()
    print(f"Название товара: {name}")

    # Закрываем сессию
    session.close()