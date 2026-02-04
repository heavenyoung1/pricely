import random
import json
import requests
from pathlib import Path
from typing import Optional

from domain.entities.proxy import Proxy
from domain.exceptions import ProxyNotFoundError
from core.logger import logger


class ProxyController:
    '''Контроллер управления прокси'''

    CHECK_URL = 'http://httpbin.org/ip'
    TIMEOUT = 10

    def __init__(
        self,
        proxy_file: str = 'infrastructure/parsers/proxy.json',
    ):
        self.proxy_file = Path(proxy_file)

    def get_proxy_if_enabled(self, enabled: bool) -> Optional[dict]:
        '''
        Возвращает прокси для Playwright если включён режим прокси.

        Args:
            enabled: Использовать прокси или нет

        Returns:
            dict в формате Playwright или None
        '''
        if not enabled:
            logger.info('Прокси выключены')
            return None
        return self.get_proxy_for_playwright()

    def get_proxy(self) -> Optional[str]:
        '''
        Загружает случайный прокси из JSON файла.

        Returns:
            Строка прокси в формате http://user:password@host:port
        '''
        try:
            if not self.proxy_file.exists():
                raise ProxyNotFoundError(
                    message=f'Файл с прокси не найден: {self.proxy_file}',
                )

            with open(
                file=self.proxy_file,
                mode='r',
                encoding='utf-8',
            ) as proxy_file:
                proxies = json.load(proxy_file)

            if not proxies:
                raise ProxyNotFoundError(
                    message='Список прокси пуст',
                )

            proxy_data = random.choice(proxies)

            proxy = Proxy(
                proxy=proxy_data['proxy'],
                user=proxy_data['user'],
                password=proxy_data['password'],
            )

            proxy_str = f'https://{proxy.user}:{proxy.password}@{proxy.proxy}'
            logger.info(f'Прокси выбран: {proxy.proxy}')

            if self.check_proxy(proxy_str):
                return proxy_str
            return None

        except json.JSONDecodeError as e:
            logger.error(f'Ошибка парсинга JSON: {e}')
            raise ProxyNotFoundError(
                message=f'Неверный формат файла прокси {e}',
                user_message='❌ Ошибка чтения файла прокси',
            )

        except KeyError as e:
            logger.error(f'Отсутствует обязательное поле в прокси: {e}')
            raise ProxyNotFoundError(
                message=f'Неверная структура данных прокси: {e}',
                user_message='❌ Ошибка структуры прокси',
            )

        except FileNotFoundError:
            logger.warning(f'Файл с прокси не найден: {self.proxy_file}')
            raise ProxyNotFoundError(
                message=f'Файл с прокси не найден: {self.proxy_file}',
                user_message='❌ Файл прокси не найден',
            )

        except ProxyNotFoundError:
            raise

        except Exception as e:
            logger.error(f'Неожиданная ошибка при получении прокси: {e}')
            raise ProxyNotFoundError(
                message=f'Unexpected error: {e}',
                user_message='❌ Ошибка при получении прокси',
            )

    def get_proxy_for_playwright(self) -> Optional[dict]:
        '''
        Возвращает прокси в формате для Playwright.

        Returns:
            dict с ключами server, username, password или None
        '''
        try:
            if not self.proxy_file.exists():
                logger.warning(f'Файл с прокси не найден: {self.proxy_file}')
                return None

            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                proxies = json.load(f)

            if not proxies:
                logger.warning('Список прокси пуст')
                return None

            proxy_data = random.choice(proxies)

            proxy_dict = {
                "server": f"https://{proxy_data['proxy']}",
                "username": proxy_data["user"],
                "password": proxy_data["password"],
            }

            logger.info(f'[PROXY] Выбран прокси: {proxy_data["proxy"]}')
            logger.debug(f'[PROXY] Полный конфиг для Playwright: {proxy_dict}')

            return proxy_dict

        except Exception as e:
            logger.error(f'Ошибка получения прокси для Playwright: {e}')
            return None
