from functools import wraps
from typing import Callable
from .unit_of_work import UnitOfWork

def with_uow(uow_factory: Callable[[], UnitOfWork], commit: bool = True):
    '''
    Декоратор для автоматического управления UnitOfWork.
    
    Args:
        uow_factory: фабрика UnitOfWork
        commit: коммитить ли транзакцию автоматически (для чтения можно отключить)
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with uow_factory() as uow:
                result = func(self, *args, uow=uow, **kwargs)
                if commit:
                    uow.commit()
                return result
        return wrapper
    return decorator