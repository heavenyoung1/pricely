import random
import json
import requests
from pathlib import Path
from typing import Optional

from domain.entities.proxy import Proxy
from domain.exceptions import ProxyNotFoundError
from core.logger import logger


class UserAgentController:
    def __init__(
        self,
        proxy_file: str = 'infrastructure/parsers/user_agents.json',
    ):
        self.proxy_file = Path(proxy_file)

    def get_user_agent(self):
        try:
            if not self.proxy_file.exists():
                raise ProxyNotFoundError(
                    message=f'Файл с UserAgent не найден: {self.proxy_file}',
                )

            with open(
                file=self.proxy_file,
                mode='r',
                encoding='utf-8',
            ) as user_agents_file:
                agents = json.load(user_agents_file)

            system = self._system()

            user_agents = agents[system]
            AGENT = random.choice(user_agents)

            return AGENT

        except json.JSONDecodeError as e:
            logger.error(f'Ошибка парсинга JSON: {e}')
            raise ProxyNotFoundError(
                message=f'Неверный формат файла с UserAgent {e}',
                user_message='❌ Ошибка чтения файла с UserAgent',
            )

    def _system(self):
        import platform

        os_name = platform.system()

        if os_name == 'Windows':
            logger.info(f'Запущено на {os_name}')
            return 'Windows'

        elif os_name == 'Linux':
            logger.info(f'Запущено на {os_name}')
            return 'Linux'

        else:
            logger.error(f'OS не обнаружена OS - {os_name}')
            raise
