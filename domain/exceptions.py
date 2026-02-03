class DatabaseError(Exception):
    pass


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f'Товар с ID={product_id} не найден')


class UserNotFoundError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f'Пользователь с ID={user_id} не найден')

class PriceNotFoundError(Exception):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f'[PARSING] Сканирование цен завершилось ошибкой! url: {url}')

class UserCreateError(Exception):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f'Не удалось создать пользователя с ID={user_id}')

class ProductCreateError(Exception):
    def __init__(self, article: str):
        self.article = article
        super().__init__(f'Не удалось создать товар (АРТИКУЛ - {article})')

class PriceCreateError(Exception):
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f'Не удалось создать цену (ID товара - {product_id})')


class ProductAlreadyExistsError(Exception):
    def __init__(self, url: str):
        self.url = url
        super().__init__(f'Товар уже отслеживается: {url}')


