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
