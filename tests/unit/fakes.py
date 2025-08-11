from typing import Dict, List, Optional
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._products: Dict[str, Product] = {}

    def save(self, product: Product) -> None:
        self._products[product.id] = product

    def get(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def delete(self, product_id: str) -> None:
        self._products.pop(product_id, None)
    
    def get_all(self) -> List[Product]:
        return list(self._products.values())


class InMemoryPriceRepository(PriceRepository):
    def __init__(self):
        self._prices: Dict[str, Price] = {}

    def save(self, price: Price) -> None:
        self._prices[price.id] = price

    def get(self, price_id: str) -> Optional[Price]:
        return self._prices.get(price_id)
    
    def delete(self, price_id: str) -> None:
        self._prices.pop(price_id, None)

    def get_all(self) -> List[Price]:
        return list(self._prices.values())

    def get_prices_by_product(self, product_id: str) -> List[Price]:
        return [p for p in self._prices.values() if p.product_id == product_id]

    def get_relevant_price_id(self, product_id: str) -> Optional[str]:
        prices = self.get_prices_by_product(product_id)
        return prices[-1].id if prices else None


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: Dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def get(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    def delete(self, user_id: str) -> None:
        self._users.pop(user_id, None)