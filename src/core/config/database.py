from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config.settings import settings


class DataBaseConnection:
    def __init__(self):
        self.engine = create_async_engine()
