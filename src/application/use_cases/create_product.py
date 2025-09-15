from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product, Price, User

from src.infrastructure.parsers import OzonParser
from datetime import datetime
import logging
import uuid
from src.infrastructure.parsers.interfaces import Parser
from src.application.interfaces import ProductParser
from src.domain.exceptions import ParserProductError, ProductCreationError

logger = logging.getLogger(__name__)

class CreateProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository,
        parser: ProductParser,
    ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo
        self.parser = parser

    def execute(self, user_id: str, url: str) -> dict:
        # 1. Парсим данные о продукте
        try:
            product_data = self.parser.parse_product(url)
            logger.info(f"Успешный парсинг данных для {url}: {product_data}")
        except Exception as e:
            logger.error(f"Ошибка парсинга URL {url} для пользователя {user_id}: {str(e)}")
            raise ParserProductError("Ошибка парсинга товара")

        # 2. Проверяем, есть ли продукт в базе
        if self.product_repo.get(product_data["id"]):
            logger.error(f"Товар с ID {product_data['id']} уже существует")
            raise ProductCreationError(f"Товар с ID {product_data['id']} уже существует")

        # 3. Создаём сущности
        product = Product(
            id=product_data["id"],
            user_id=user_id,
            name=product_data["name"],
            link=url,
            image_url=product_data["image_url"],
            rating=product_data["rating"],
            categories=product_data["categories"],
        )

        price = Price(
            id=None,  # БД сама создаст автоинкрементный id
            product_id=product.id,
            with_card=product_data["price_with_card"],
            without_card=product_data["price_without_card"],
            previous_with_card=None,
            previous_without_card=None,
            default=product_data["price_default"],
            created_at=datetime.now(),
        )

        # 4. Работаем с пользователем
        user = self.user_repo.get(user_id)
        is_new_user = not user

        if is_new_user:
            user = User(
                id=user_id,
                username="unknown",
                chat_id=user_id,
                products=[product.id],
            )
            self.user_repo.save(user)
        else:
            if product.id not in user.products:
                user.products.append(product.id)
                self.user_repo.save(user)

        # 5. Сохраняем продукт и цену
        try:
            self.product_repo.save(product)
            self.price_repo.save(price)
        except Exception as e:
            logger.error(f"Ошибка сохранения товара {product.id}: {e}")
            raise ProductCreationError("Ошибка сохранения товара")

        return {
            "product_id": product.id,
            "product_name": product.name,
            "user_id": product.user_id,
        }