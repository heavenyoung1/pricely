import json
import random
from typing import Optional

from .options import user_agents
from core.logger import logger


class BrowserEngine:
    def __init__(
        self,
        headless: bool = False,
        user_agent: Optional[str] = None,
        proxy: Optional[str] = None,
        wait_time: int = 5,
    ):
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent or self.set_user_agent()

    def _get_user_agent(self) -> str:
        '''Загружает список User-Agent из файла и выбирает случайный'''
        try:
            index = randrange(len(user_agents))
            user_agent = user_agents[index]
            logger.info(f'UserAgent успешно получен: {user_agent}')
            return user_agent
        except Exception as e:
            logger.error(f'Ошибка получения UserAgent: {e}')
            raise
