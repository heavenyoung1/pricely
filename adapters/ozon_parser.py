from domain.repositories.product_repository import ProductRepository
from adapters.session_engine import SessionEngine
from adapters.selenium_adapter import SeleniumAdapter
from domain.entities.product import Product
from utils.logger import logger

from typing import List

class OzonParserUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def calculate_discount(self, price_without_card: int, price_default: int) -> int:
        """Вычисляет размер скидки в процентах."""
        if price_default > 0 and price_without_card > 0:
            discount = int(((price_default - price_without_card) / price_default) * 100) // 1
            logger.info(f"Размер скидки составляет: {discount}%")
            return discount
        return 0
    
    def execute(self, url: str) -> Product:
        """Выполняет полный парсинг товара с указанной страницы."""
        try:
            # Предполагаем, что repository реализует навигацию
            product_data = self.repository.get_product_data(url)
            discount_amount = self.calculate_discount(product_data.price_without_card, product_data.price_default)
            product = Product(
                id=product_data.id,
                name=product_data.name,
                rating=product_data.rating,
                price_with_card=product_data.price_with_card,
                price_without_card=product_data.price_without_card,
                price_default=product_data.price_default,
                discount_amount=discount_amount,
                link=url,
                url_image=product_data.url_image,
                category_product=product_data.category_product
            )
            logger.info(f"Успешно создан объект Product: {product}")
            return product
        except Exception as e:
            logger.error(f"Ошибка при полном парсинге: {e}")
            return Product("N/A", "N/A", 0.0, 0, 0, 0, 0.0, url, "N/A", [])


# Тестирование функции
if __name__ == "__main__":
    session = SessionEngine(headless=True)
    selenium_adapter = SeleniumAdapter(session)
    ozon_parser = OzonParserUseCase(selenium_adapter)
    product = ozon_parser.execute('https://www.ozon.ru/product/ketchup-maheev-tomatnyy-500-g-138349705/')
    print(f"Получен продукт: {product}")
    session.close()