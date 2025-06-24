from functools import wraps
from utils.logger import logger

class BaseParser:
    def __init__(self, driver:):
        self.driver = driver
        self.timeout = 10
    
    def _logs_errors(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f'Ошибка в {func.__name__}: {str(e)}')
                raise
        return wrapper