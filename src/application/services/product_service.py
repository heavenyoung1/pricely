import logging
logger = logging.getLogger(__name__)

from src.domain.entities import Product, Price, User
from src.interfaces.repositories import ProductRepository, PriceRepository, UserRepository

class ProductService:
    def __init__(
            self, 
            product_repository: ProductRepository,
            price_repository: PriceRepository,
            user_repository: UserRepository,
    ):
        self.product_repository = product_repository,
        self.price_repository = price_repository,
        self.user_repository = user_repository

    def create_product(self, product: Product, price: Price, user: User) -> Product:
        '''Создаёт или обновляет продукт, цену и пользователя.'''
        self.price_repository.save_
        
