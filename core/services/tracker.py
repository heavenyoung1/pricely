from datetime import datetime
from typing import Dict

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
            # Проверяем, существует ли уже товар
            being_product = self.product_repo.find_by_url(url)
            if being_product:
                user.subscribe(being_product)
                await self.user_repo.save(user)
                await self.notifier.notify(user, f'Вы, {user.telegram_id}, подписаны на товар {being_product.name}')
                return
            
            # Парсим товар
            parser = self.parser_factory.get_parser(url)
            product_info = await parser.parse(url)

            # Создаём новый товар
            product = Product(
                id=product_info.id, #Далее переопределить метод для парсинга ID товара
                name=product_info.name,
                url=product_info.url,
                marketplace=parser.get_marketplace(),
                last_price=product_info.last_price,
                image_url=product_info.image_url,
            )

            # Сохраняем товар и подписку пользователя
            await self.product_repo.save(product)
            user.subscribe(product)
            await self.user_repo.save(product)

            # Уведомляем пользователя о подписке
            await self.notifier.notify(user, f'Добавлен товар для отслеживания f{product.name}')
        except Exception as e:
            error_msg = f'Ошибка при добавлении товара {product.name}'
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
                            id='1',
                            product_id=product.id,
                            price=product.price,
                            timestamp=datetime.now()
                        )
                        await self.price_repo.save(price)
                except Exception as e:
                    logger.error(f'Ошибка при парсинге {product.url}: {str(e)}')
        except Exception as e:
            logger.error(f'Ошибка при проверке цен: {str(e)}')
            raise RuntimeError(f'Ошибка при процерке цен: {str(e)}')


    async def notify_users(self, product: Product, price_change: Dict) -> None:
        '''  '''
        try:
            users = await self.user_repo.find_all() 
            for user in users:
                if product in user.subscribe:
                    message = (
                        f'Цена на товар '{product.name}' изменилась!\n'
                        f'Старая цена: {price_change['old_price']} ₽\n'
                        f'Новая цена: {price_change['new_price']} ₽\n'
                        f'Ссылка: {product.url}'
                    ) 
                    await self.notifier.notify(user, message)
        except Exception as e:
            logger.error(f'Ошибка при уведомлении пользователей: {str(e)}')
            raise RuntimeError(f'Ошибка при уведомлении: {str(e)}')

