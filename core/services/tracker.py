from core.interfaces.notifier import INotifier
from core.interfaces.parser import IProductParserFactory
from core.interfaces.product import IProductRepo
from core.interfaces.user import IUserRepo
from core.models.user import User
from core.models.product import Product

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
        """ Добавляет товар на отслеживание для пользователя """
        try:
            # Проверяем, существует ли уже товар
            being_product = self.product_repo.find_by_url(url)
            if being_product:
                user.follow(being_product)
                self.user_repo.save(user)
                self.notifier.notify(user, f'Вы, {user.telegram_id}, подписаны на товар {being_product.na}')
                return
            
            # Парсим товар
            parser = self.parser_factory.get_parser(url)
            product_info = parser.parse(url)

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
            self.product_repo.save(product)
            user.follow(product)
            self.user_repo.save(product)

            # Уведомляем пользователя о подписке
            self.notifier.notify(user, f'Добавлен товар для отслеживания f{product.name}')
        except Exception as e:
            error_msg = f'Ошибка при добавлении товара {product.name}'
            raise RuntimeError(error_msg)

    def check_price():
        pass



