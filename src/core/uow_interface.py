from abc import ABC, abstractmethod
from src.infrastructure.database.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl

class UnitOfWork(ABC):
    '''Абстрактный базовый класс для Unit of Work.'''
    # Эти аннотации типов говорят, что у UoW будут такие атрибуты
    products: 'ProductRepositoryImpl'
    prices: 'PriceRepositoryImpl'
    users: 'UserRepositoryImpl'

    # Магические методы для контекстного менеджера (with statement)
    def __enter__(self):
        '''Вход в контекстный менеджер.'''
        return self  # Возвращает сам объект UoW при входе в контекст
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Выход из контекстного менеджера.'''
        # exc_type - тип исключения (None если нет ошибки)
        # exc_val - значение исключения (объект исключения)
        # exc_tb - traceback исключения
        if exc_type is not None:    # Если была ошибка
            self.rollback()         # Откатываем транзакцию
        else:
            self.commit()           # Иначе коммитим изменения

    @abstractmethod # Этот метод ДОЛЖЕН быть реализован в дочерних классах
    def commit(self):
        '''Фиксация всех изменений'''
        pass

    @abstractmethod # Этот метод ДОЛЖЕН быть реализован в дочерних классах
    def rollback(self):
        '''Откат всех изменений'''
        pass