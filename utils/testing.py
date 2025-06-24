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

    async def track_product(self, user, url):
        # 1. Проверка: есть ли товар в базе
        being_product = self.product_repo.find_by_url(url)

        if being_product:
            user.subscribe(being_product)
            self.user_repo.save(user) #ЗАЧЕМ НАМ ТАБЛИЦА С ПОЛЬЗОВАТЕЛЯМИ, НУ ОК?
            self.notifier.notify(user, f'Вы подписались на товар')

        parser = self.parser_factory.