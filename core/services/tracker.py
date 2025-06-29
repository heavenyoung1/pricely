from datetime import datetime
from typing import Dict
from uuid import uuid4

from core.interfaces.notifier import INotifier
from core.interfaces.parser import IProductParserFactory
from core.interfaces.product import IProductRepo
from core.interfaces.user import IUserRepo
from core.interfaces.price import IPriceRepo
from core.models.user import User
from core.models.product import Product
from core.models.price import Price
from utils.logger import logger

class ProductTracker:
    def __init__(
            self, 
            user_repo: IUserRepo,
            product_repo: IProductRepo,
            notifier: INotifier,
            parser_factory: IProductParserFactory,
            price_repo: IPriceRepo,
            ):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.notifier = notifier
        self.parser_factory = parser_factory
        self.price_repo = price_repo

    async def track_product(self, user: User, url: str) -> None:
        ''' Добавляет товар на отслеживание для пользователя '''
        try:
            # Проверяем, существует ли такой товар
            being_product = await self.product_repo.find_by_url(url)
            if being_product:
                user.subscribe(being_product)
                await self.user_repo.save(user)
                await self.notifier.notify(user, f'Вы, подписаны на товар {being_product.name}')
                return
            
            # Парсим и создаём товар
            product = await self.parse_product(url)
            await self.product_repo.save(product)

            user.subscribe(product)
            await self.user_repo.save(user)
            await self.notifier.notify(user, f'Добавлен товар для отслеживания: {product.name}')

        except Exception as e:
            error_msg = f"Ошибка при добавлении товара: {str(e)}"
            logger.error(error_msg)
            await self.notifier.notify(user, error_msg)
            raise RuntimeError(error_msg)

    async def check_price(self) -> None:
        ''' Проверяет цены всех отслеживаемых товаров '''
        try:
            products = await self.product_repo.find_all()
            for product in products:
                parser = self.parser_factory.get_parser(product.url)
                try:
                    product_info = await parser.parse(product.url)
                    price_change = product.update_price(product_info.last_price)
                    if price_change['changed'] == True:
                        await self.product_repo.save(product)

                        # Сохраняем историю цены
                        price = Price(
                            id=str(uuid4()),
                            product_id=product.id,
                            price=price_change['new_price'],
                            timestamp=datetime.now()
                        )
                        await self.price_repo.save(price)
                        await self.notify_users(product, price_change)
                except Exception as e:
                    logger.error(f'Ошибка при парсинге {product.url}: {str(e)}')
        except Exception as e:
            logger.error(f'Ошибка при проверке цен: {str(e)}')
            raise RuntimeError(f'Ошибка при процерке цен: {str(e)}')


    async def notify_users(self, product: Product, price_change: Dict) -> None:
        ''' Уведомляет подписанных пользователей об изменении цены '''
        try:
            users = await self.user_repo.find_by_product_id(product.id) 
            for user in users:
                if product in user.subscribe:
                    message = (
                        f"Цена на товар '{product.name}' изменилась!\n"
                        f"Старая цена: {price_change['old_price']} ₽\n"
                        f"Новая цена: {price_change['new_price']} ₽\n"
                        f"Ссылка: {product.url}"
                    )
                    await self.notifier.notify(user, message)
        except Exception as e:
            logger.error(f'Ошибка при уведомлении пользователей: {str(e)}')
            raise RuntimeError(f'Ошибка при уведомлении: {str(e)}')

    async def parse_product(self, url: str) -> Product:
        ''' '''
        parser = self.parser_factory.get_parser(url)
        product_info = await parser.parse(url)
        return Product(
            id=product_info.id,
            name=product_info.name,
            url=product_info.url,
            marketplace=parser.get_marketplace(),
            last_price=product_info.last_price,
            image_url=product_info.image_url
        )