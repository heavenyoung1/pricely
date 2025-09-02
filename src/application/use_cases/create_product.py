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
        try:
            product_data = self.parser.parse_product(url)
            logger.info(f'Успешный парсинг данных для {url}: {product_data}')
        except Exception as e:
            logger.error(f'Ошибка парсинга URL {url} для пользователя {user_id}: {str(e)}')
            raise ParserProductError(f'Ошибка парсинга товара')

        price_id = str(uuid.uuid4())

        # Создание доменных сущностей
        product = Product(
            id=product_data['id'],
            user_id=user_id,
            price_id=price_id,
            name=product_data['name'],
            link=url,
            image_url=product_data['image_url'],
            rating=product_data['rating'],
            categories=product_data['categories']
        )

        price = Price(
            id=price_id,
            product_id=product.id,
            with_card=product_data['price_with_card'],
            without_card=product_data['price_without_card'],
            previous_with_card=None,
            previous_without_card=None,
            default=product_data['price_default'],
            claim=datetime.now()
        )

        # Проверяем существование пользователя один раз
        user = self.user_repo.get(user_id)
        is_new_user = not user  # Запоминаем, новый ли пользователь
        if is_new_user:
            logger.debug(f'Создание нового пользователя {user_id}')
            user = User(
                id=user_id,
                username='unknown',
                chat_id=user_id,
                products=[],
            )

        # Проверяем существование продукта
        existing_product = self.product_repo.get(product.id)
        if existing_product:
            logger.error(f'Товар с ID {product.id} уже существует')
            raise ProductCreationError(f'Товар с ID {product.id} уже существует')

        # Сохранение
        try:
            if is_new_user:
                logger.debug(f'Сохранение нового пользователя {user_id}')
                self.user_repo.save(user)
            self.product_repo.save(product)
            self.price_repo.save(price)
            user.products.append(product.id)
            logger.debug(f'Обновление списка продуктов для пользователя {user_id}')
            self.user_repo.save(user)
            logger.info(f'Товар {product.name} сохранён для пользователя {user_id}')
        except Exception as e:
            logger.error(f'Ошибка сохранения в БД для {url} от пользователя {user_id}: {str(e)}')
            raise ProductCreationError(f'Ошибка сохранения товара')

        return {
            'id': product.id,
            'name': product.name,
            'user_id': product.user_id,
            'price_id': product.price_id
        }