from typing import Callable, Awaitable
import asyncio

import redis.asyncio as redis

from core.config.settings import settings
from core.logger import logger
from infrastructure.redis.message import NotificationMessage


class NotificationSubscriber:
    '''
    Слушает Redis очередь и обрабатывает уведомления.

    Используется ботом для получения уведомлений от чекера.
    '''

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._queue_name = settings.REDIS_QUEUE_NAME
        self._running = False

    async def connect(self) -> None:
        '''Подключиться к Redis'''
        if self._redis is None:
            self._redis = redis.from_url(settings.redis_url)
        logger.info('Subscriber подключен к Redis')

    async def close(self) -> None:
        '''Закрыть соединение'''
        self._running = False
        if self._redis:
            await self._redis.close()
            logger.info('Subscriber отключен от Redis')

    async def listen(
        self,
        handler: Callable[[NotificationMessage], Awaitable[None]],
        timeout: int = 5,
    ) -> None:
        '''
        Слушать очередь и обрабатывать сообщения.

        Args:
            handler: Асинхронная функция для обработки сообщения.
            timeout: Таймаут ожидания сообщения (секунды).
        '''
        self._running = True
        logger.info(f'Начинаю слушать очередь: {self._queue_name}')

        while self._running:
            try:
                # BRPOP блокирует до получения сообщения или таймаута
                result = await self._redis.brpop(self._queue_name, timeout=timeout)

                if result is None:
                    continue

                _, raw_message = result
                message = NotificationMessage.model_validate_json(raw_message)

                try:
                    await handler(message)
                except Exception as e:
                    logger.error(f'Ошибка обработки уведомления: {e}')
                    # TODO: можно добавить dead letter queue

            except asyncio.CancelledError:
                logger.info('Listener остановлен')
                break
            except Exception as e:
                logger.error(f'Ошибка получения сообщения из Redis: {e}')
                await asyncio.sleep(1)

    def stop(self) -> None:
        '''Остановить слушателя'''
        self._running = False

    async def __aenter__(self) -> 'NotificationSubscriber':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
