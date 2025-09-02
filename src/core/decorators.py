from functools import wraps
from src.core import get_db_session, UnitOfWork


def with_uow(commit: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with get_db_session() as session:
                with UnitOfWork(lambda: session) as uow:
                    result = func(self, *args, uow=uow, **kwargs)
                    if commit:
                        uow.commit()
                    return result
        return wrapper
    return decorator