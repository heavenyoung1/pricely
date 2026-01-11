import random
import json
import requests
from pathlib import Path
from typing import Optional

from src.domain.entities.proxy import Proxy
from src.core.logger import logger


class ProxyController:
    '''Контроллер управления прокси'''
    CHECK_URL = 'http://httpbin.org/ip'  # Надежный сервис для проверки
    TIMEOUT = 10  # Таймаут проверки

    def __init__(
        self, 
        proxy_file: str = 'src/infrastructure/parsers/proxy.json',
    ):
        self.proxy_file = Path(proxy_file)

    def get_proxy_if_enabled(self, enabled: bool) -> Optional[str]:
        if not enabled:
            logger.info(f'Прокси выключены')
            return None
        return self.get_proxy()

    def get_proxy(self) -> Optional[str]:
        try:
            # 1. Проверка существования файла
            if not self.proxy_file.exists():
                raise ProxyNotFoundError(
                    message=f'Файл с прокси не найден: {self.proxy_file}',
                )
            
            # 2. Загрузка JSON
            with open(
                file=self.proxy_file,
                mode='r',
                encoding='utf-8',
            ) as proxy_file:
                proxies = json.load(proxy_file)

            # 3. Проверка на пустой список
            if not proxies:
                raise ProxyNotFoundError(
                    message='Список прокси пуст',
                )

            proxy_data = random.choice(proxies)

            # Создание Domain сущности
            proxy = Proxy(
                proxy=proxy_data['proxy'],
                user=proxy_data['user'],
                password=proxy_data['password']
            )   

            proxy_str = f'http://{proxy.user}:{proxy.password}@{proxy.proxy}'
            logger.info(f'Прокси успешно получен: {proxy_str}')

            success = self.check_proxy(proxy_str)
            if success:
                return proxy_str
                return None

        except json.JSONDecodeError as e:
            logger.error(f'Ошибка парсинга JSON: {e}')
            raise ProxyNotFoundError(
                message=f'Неверный формат файла прокси {e}',
                user_message='❌ '
            )
        
        except KeyError as e:
            logger.error(f'Отсутствует обязательное поле в прокси: {e}')
            raise ProxyNotFoundError(
                message=f'Неверная структура данных прокси: {e}',
                user_message='❌ '
            )
        
        except FileNotFoundError:
            logger.warning(f'Файл с прокси не найден: {self.proxy_file}')
            raise ProxyNotFoundError(
                message=f'Файл с прокси не найден: {self.proxy_file}',
                user_message='❌ '
            )
        
        except Exception as e:
            logger.error(f'Неожиданная ошибка при получении прокси: {e}')
            raise ProxyNotFoundError(
                message=f'Unexpected error: {e}',
                user_message='❌ Ошибка при получении прокси'
            )
        
    def check_proxy(self, proxy: str) -> bool:
        response = requests.get(
            url='https://8.8.8.8',
            proxies=proxy,
        )
        if response.status_code == 200:
            logger.info(
                f'Прокси успешно проверены, StatusCode {response.status_code}'
                )
            return True
        else:
            logger.info(
                f'Прокси нерабочие, StatusCode {response.status_code}'
                )
            return False
    