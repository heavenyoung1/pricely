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
        if product_id in self.products:
            del self.products[product_id]
    
    def get_all(self) -> list[Product]:
        return list(self._storage.values())

class InMemoryPriceRepository(PriceRepository):
    def __init__(self):
        self.prices: Dict[str, Price] = {}

    def save(self, price: Price):
        self.prices[price.id] = price

    def get(self, price_id: str):
        return self.prices.get(price_id)

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: Dict[str, User] = {}

    def save(self, user: User):
        self.users[user.id] = user

    def get(self, user_id: str):
        return self.users.get(user_id)