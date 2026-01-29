import json
import random
from pathlib import Path
from typing import Optional

from domain.entities.proxy import Proxy
from domain.exceptions import ProxyNotFoundError
from core.logger import logger


class ProxyRepository:
    def __init__(
        self,
        proxy_file_path: str = 'src/infrastructure/parsers/proxy.json',
        encoding='utf-8',
    ):
        self.proxy_file_path = Path(proxy_file_path)

    # async def get_random(self) -> 'Proxy':
    #     proxies = self.
