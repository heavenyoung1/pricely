class DomainException(Exception):
    '''Базовое доменное исключение'''

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ProductNotFoundError(DomainException):
    '''Товар не найден'''

    def __init__(self, product_id: int):
        super().__init__(
            message=f'Товар с ID = {product_id} не найден',
        )


class UserNotFoundError(DomainException):
    '''Пользователь не найден'''

    def __init__(self, user_id: int):
        super().__init__(
            message=f'Пользователь с ID = {user_id} не найден',
        )

class ProxyNotFoundError(DomainException):
    '''Исключение: прокси не найдены или не работают'''
    
    def __init__(self, message: str):
        super().__init__(
            message='Не удалось получить рабочий прокси',
        )


class DatabaseError(DomainException):
    '''Ошибка работы с БД'''

    pass
