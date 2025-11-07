from src.application.interfaces.repositories import (
    ProductRepository,
    PriceRepository,
    UserRepository,
    UserProductsRepository,
)
from src.domain.entities import Product, Price, User
from src.infrastructure.parsers import OzonParser
from datetime import datetime
import logging
import uuid
import re
from src.infrastructure.parsers.interfaces import Parser
from src.application.interfaces import ProductParser
from src.domain.exceptions import ParserProductError, ProductCreationError

logger = logging.getLogger(__name__)


class CreateProductUseCase:
    """
    Use case для создания нового товара.

    Этот класс отвечает за:
    - парсинг данных о товаре,
    - проверку наличия товара в базе данных,
    - создание новых сущностей товара и цены,
    - привязку товара к пользователю,
    - сохранение данных в базе данных.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository,
        user_products_repo: UserProductsRepository,
        parser: ProductParser,
    ):
        """
        Инициализация UseCase для создания нового товара.

        :param product_repo: Репозиторий для работы с продуктами.
        :param price_repo: Репозиторий для работы с ценами.
        :param user_repo: Репозиторий для работы с пользователями.
        :param user_products_repo: Репозиторий для работы с привязками пользователей и товаров.
        :param parser: Парсер для получения данных о товаре с внешнего ресурса.
        """
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo
        self.user_products_repo = user_products_repo
        self.parser = parser

    def execute(self, user_id: str, url: str) -> dict:
        """
        Основной метод для выполнения логики создания товара.

        1. Парсит данные о товаре с помощью парсера.
        2. Проверяет, существует ли товар с таким ID в базе данных.
        3. Создаёт сущности товара и цены.
        4. Привязывает товар к пользователю.
        5. Сохраняет товар и цену в базе данных.

        :param user_id: Идентификатор пользователя, для которого создается товар.
        :param url: Ссылка на страницу товара для парсинга.
        :return: Словарь с полными данными о товаре и цене.
        :raises ParserProductError: Если произошла ошибка при парсинге данных о товаре.
        :raises ProductCreationError: Если произошла ошибка при создании товара.
        """
        logger.debug(f"🔗 в CreateProductUseCase передан текст {url}")
        # 1. Проверяем, является ли URL ссылкой или текстом с ссылкой
        valid_url = exctract_link(url)
        logger.info(f"🔗 Обрабатываем ссылку {valid_url}")
        # 1. Парсим данные о товаре
        try:
            product_data = self.parser.parse_product(valid_url)
            logger.info(f"Парсинг данных для {valid_url}: {product_data} завершен.")
        except Exception as e:
            logger.error(
                f"Ошибка парсинга URL {valid_url} для пользователя {user_id}: {str(e)}"
            )
            raise ParserProductError("Ошибка парсинга товара")

        # 2. Проверяем, есть ли товар в БД
        if self.product_repo.get(product_data["id"]):
            logger.error(f'Товар с ID {product_data["id"]} уже существует')
            raise ProductCreationError(
                f'Товар с ID {product_data["id"]} уже существует'
            )

        # 3. Создаём сущности
        product = Product(
            id=product_data["id"],
            user_id=user_id,
            name=product_data["name"],
            link=valid_url,
        )

        price = Price(
            id=None,  # автоинкрементированный ID, создаваемый в БД
            product_id=product.id,
            with_card=product_data["price_with_card"],
            without_card=product_data["price_without_card"],
            previous_with_card=None,
            previous_without_card=None,
            created_at=datetime.now(),
        )

        # Добавляем цену к товару
        product.prices.append(price)

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

        # 5. Сохраняем товар и цену
        try:
            self.product_repo.save(product)
            self.price_repo.save(price)

            # 6. Создаём связь user <-> product в таблице user_products
            self.user_products_repo.add_product_for_user(user_id, product.id)
        except Exception as e:
            logger.error(f"Ошибка сохранения товара {product.id}: {e}")
            raise ProductCreationError("Ошибка сохранения товара")

        # 7. Возвращаем полные данные для удобства
        return {
            "product_id": product.id,
            "product_name": product.name,
            "user_id": product.user_id,
            "link": product.link,
            "with_card": price.with_card,
            "without_card": price.without_card,
        }


def is_url(text):
    """Проверяет, начинается ли строка с https://"""
    pattern = r"^https?://"
    return bool(re.match(pattern, text))


def exctract_link(text: str) -> str:
    """
    Проверяет, является ли переданный текст ссылкой на Ozon. Если это не ссылка,
    извлекает ссылку из текста.

    :param input_str: Строка, которая может быть ссылкой или содержать ссылку.
    :return: Ссылка на товар на Ozon.
    :raises ValueError: Если в строке не найдено валидной ссылки на Ozon.
    """
    if is_url(text):
        return text

    listing = text.split()
    url = listing[-1]
    return url
