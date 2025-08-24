from functools import wraps
from src.infrastructure.database.core import get_db_session, UnitOfWork

def with_uow(commit: bool = False):
    '''
    Декоратор для сервисных методов, автоматически создающий UnitOfWork.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with get_db_session() as session:   # создаём сессию
                with UnitOfWork(lambda: session) as uow:  # оборачиваем её в UoW
                    result = func(self, *args, uow=uow, **kwargs)
                    if commit:
                        uow.commit()
                    return result
        return wrapper
    return decorator