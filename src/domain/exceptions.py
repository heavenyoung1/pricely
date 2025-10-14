class ApplicationError(Exception):
    '''Базовое исключение уровня приложения.'''
    pass

class ParserProductError(ApplicationError):
    '''Ошибка при парсинге товара.'''
    pass


# --- User ---
class UserCreationError(ApplicationError):
    '''Ошибка при создании пользователя.'''
    pass

class ProductNotExistingDataBase(ApplicationError):
    '''Ошибка, возникающая, когда продукт не существует в базе данных.'''
    pass


# --- Product ---
class ProductError(ApplicationError):
    '''Базовое исключение для работы с продуктами.'''
    pass


class ProductCreationError(ProductError):
    '''Ошибка при создании продукта.'''
    pass

class ProductSavingError(ProductError):
    '''Ошибка при сохранении продукта.'''
    pass


class ProductNotFoundError(ProductError):
    '''Ошибка, возникающая, когда продукт не найден в базе данных.'''
    pass


class ProductDeletingError(ProductError):
    '''Ошибка при удалении продукта.'''
    pass


# --- Price ---
class PriceError(ApplicationError):
    '''Базовое исключение для работы с ценами.'''
    pass


class PriceUpdateError(PriceError):
    '''Ошибка при обновлении цены.'''
    pass
