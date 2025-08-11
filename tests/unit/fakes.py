from typing import Dict
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def save(self, product: Product):
        self.products[product.id] = product

    def get(self, product_id: str):
        return self.products.get(product_id)

    def delete(self, product_id: str):
        self.products.pop(product_id, None)
    
    def get_all(self) -> list[Product]:
        return list(self.products.values())


class InMemoryPriceRepository(PriceRepository):
    def __init__(self):
        self.prices: Dict[str, Price] = {}

    def save(self, price: Price):
        self.prices[price.id] = price

    def get(self, price_id: str):
        return self.prices.get(price_id)
    
    def delete(self, price_id: str) -> None:
        self.prices.pop(price_id, None)

    def get_all(self) -> list[Price]:
        return list(self.prices.values())

    def get_prices_by_product(self, product_id: str) -> list[Price]:
        return [p for p in self.prices.values() if p.product_id == product_id]

    def get_relevant_price_id(self, product_id: str) -> str | None:
        prices = self.get_prices_by_product(product_id)
        return prices[-1].id if prices else None


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}

    def save(self, user: User):
        self.users[user.id] = user

    def get(self, user_id: str):
        return self.users.get(user_id)
    
    def delete(self, user_id: str):
        self.users.pop(user_id, None)