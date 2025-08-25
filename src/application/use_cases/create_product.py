from src.domain.repositories import UserRepository, ProductRepository, PriceRepository
from src.domain.entities import Product, Price, User
from src.infrastructure.core.ozon_parser import OzonParser
from datetime import datetime
import logging
import uuid
from src.domain.interfaces.product_parser import IProductParser

logger = logging.getLogger(__name__)

class CreateProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository,
        parser: IProductParser,   # <-- абстракция
    ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo
        self.parser = parser      # <-- конкретика подставляется извне


    def execute(self, user_id: str, url: str) -> dict:
        try:
            product_data = self.parser.parse_product(url)
            logger.info(f'Успешный парсинг данных для {url}: {product_data}')
        except Exception as e:
            logger.error(f'Ошибка парсинга URL {url} для пользователя {user_id}: {str(e)}')
            raise
        
        price_id = str(uuid.uuid4()) # price_id нужен для нескольких таблиц, создается здесь

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
            previous_with_card=None,       # ОТКУДА ВЗЯТЬ ВОТ ЭТО?
            previous_without_card=None,    # ОТКУДА ВЗЯТЬ ВОТ ЭТО?
            default=product_data['price_default'],
            claim=datetime.now()
        )

        user = self.user_repo.get(user_id) or User(
            id=user_id, 
            username='unknown', 
            chat_id=user_id, 
            products=[],
        )

        # Сохранение
        try:
            if not self.user_repo.get(user_id):
                self.user_repo.save(user)
            self.product_repo.save(product)
            self.price_repo.save(price)
            # Обновление списка продуктов пользователя (если нужно)
            user.products.append(product)
            self.user_repo.save(user)
            logger.info(f'Товар {product.name} сохранён для пользователя {user_id}')
        except Exception as e:
            logger.error(f'Ошибка сохранения в БД для {url} от пользователя {user_id}: {str(e)}')