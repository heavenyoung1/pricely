import re

from infrastructure.database.unit_of_work import UnitOfWorkFactory

from application.tools.adapter import LinkAdapter
from application.interfaces.parser import IProductParser
from domain.entities.product import Product, FullProduct
from domain.entities.price import Price

from domain.exceptions import ProductAlreadyExistsError
from core.logger import logger


class AddProductUseCase:
    '''
    Use Case для добавления нового товара в отслеживание.

    Парсит страницу товара, создаёт записи Product и Price,
    и связывает товар с пользователем.
    '''

    def __init__(
        self,
        parser: IProductParser,
        uow_factory: UnitOfWorkFactory,
    ) -> None:
        self.parser = parser
        self.uow_factory = uow_factory

    async def execute(
        self,
        url: str,
        user_id: int,
        change: int,
    ) -> Product:
        '''
        Добавляет товар по URL для указанного пользователя.

        Args:
            url: URL страницы товара.
            user_id: ID пользователя, добавляющего товар.

        Returns:
            Созданный Product.

        Raises:
            ProductAlreadyExistsError: Если товар уже отслеживается этим пользователем.
        '''
        # 1. Преобразуем ссылку в нужный формат
        # valid_url = await LinkAdapter.exctract_link(url)

        # 2. Парсим данные со страницы
        parsed = await self.parser.parse_new_product(url)
        logger.info(f'В браузере получен товар: {parsed.name}')

        async with self.uow_factory.create() as uow:
            # 3. Проверяем, не существует ли уже такой товар
            existing = await uow.product_repo.get_by_link(url)
            if existing:
                # Проверяем, отслеживает ли уже этот пользователь
                user_product_ids = await uow.user_products_repo.get_all_by_user(user_id)
                if existing.id in user_product_ids:
                    raise ProductAlreadyExistsError(url)

                # Товар есть, но пользователь его не отслеживает — связываем
                await uow.user_products_repo.save(user_id, existing.id)
                logger.info(f'Товар привязан к пользователю: {existing.name}')
                return existing

            # 4. Создаём новый товар
            product = Product.create(
                article=parsed.article,
                name=parsed.name,
                link=parsed.link,
                change=change,
            )
            saved_product = await uow.product_repo.save(product)

            # 5. Создаём начальную цену
            price = Price.create(
                product_id=saved_product.id,
                with_card=parsed.price_with_card,
                without_card=parsed.price_without_card,
                previous_with_card=parsed.price_with_card,
                previous_without_card=parsed.price_without_card,
            )
            await uow.price_repo.save(price)

            # 6. Связываем товар с пользователем
            await uow.user_products_repo.save(user_id, saved_product.id)

            logger.info(
                f'Товар добавлен: {saved_product.name} (ID: {saved_product.id})'
            )

            return FullProduct(
                id=product.id,
                article=product.article,
                name=product.name,
                link=product.link,
                price_with_card=price.with_card,
                price_without_card=price.without_card,
                price_previous_with_card=price.previous_with_card,
                price_previous_without_card=price.previous_without_card,
                change=product.change,
            )


def is_url(text):
    '''Проверяет, начинается ли строка с https://'''
    pattern = r'^https?://'
    return bool(re.match(pattern, text))


def exctract_link(text: str) -> str:
    '''
    Проверяет, является ли переданный текст ссылкой на Ozon. Если это не ссылка,
    извлекает ссылку из текста.

    :param input_str: Строка, которая может быть ссылкой или содержать ссылку.
    :return: Ссылка на товар на Ozon.
    :raises ValueError: Если в строке не найдено валидной ссылки на Ozon.
    '''
    if is_url(text):
        return text

    listing = text.split()
    url = listing[-1]
    logger.debug(f'[URL] ПОЛУЧЕНА ССЫЛКА {url}')
    return url
