class BaseCustomException(Exception):
    '''Базовый класс для всех исключений в приложении.'''

    def __init__(self, message: str = 'Произошла ошибка'):
        self.message = message
        super().__init__(self.message)

class EntityNotFoundException(BaseCustomException):
    '''Ошибка, когда сущность не найдена.'''
