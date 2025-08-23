from src.interfaces.dto import ProductDTO, PriceDTO

class ProductFormatter:
    @staticmethod
    def added(product: ProductDTO) -> str:
        return (
            f'<b>✅ Товар добавлен!</b>\n\n'
            f'<b>Название:</b> {product.name}\n'
            f'<b>ID:</b> {product.id}\n'
            f'<b>Рейтинг:</b> {product.rating}\n'
            f'<b>Цена с картой:</b> {product.price_with_card}\n'
            f'<b>Цена без карты:</b> {product.price_without_card}\n'
            f'<b>Базовая цена:</b> {product.price_default}\n'
            f'<b>Категории:</b> {', '.join(product.categories)}'   
        )
    
    @staticmethod
    def price_changed(product: ProductDTO, price: PriceDTO) -> str:
        return (
            f'📉 Цена изменилась!\n\n'
            f'{product.name}\n'
            f'Предыдущая цена: {price.previous_with_card}\n'
            f'Актуальная цена: {price.with_card}'
        )