from abc import ABC, abstractmethod

class UnitOfWork(ABC):
    '''Абстрактный базовый класс для Unit of Work'''
    products: 'ProductRepositoryImpl'
    prices: 'PriceRepositoryImpl'
    users: 'UserRepositoryImpl'

    def __enter__(self):
        return self
