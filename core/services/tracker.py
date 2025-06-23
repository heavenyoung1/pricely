from core.interfaces.notifier import INotifier
from core.interfaces.parser import IProductParserFactory
from core.interfaces.product import IProductRepo
from core.interfaces.user import IUserRepo
from core.models.user import User

class ProductTracker:
    def __init__(
            self, 
            user_repo: IUserRepo,
            product_repo: IProductRepo,
            notifier: INotifier,
            parser_factory: IProductParserFactory
            ):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.notifier = notifier
        self.parser_factory = parser_factory

    def track_product(self, user: User, url: str) -> None:
        being_product = self.product_repo.find_by_url(url)
        if being_product:
            user.follow(being_product)
            self.user_repo.save(user)
            self.notifier.notify(user, f'Вы, {user.telegram_id}, подписаны на товар {being_product.na}')
            return
        
        # Парсим товар
        parser = self.parser_factory.get


