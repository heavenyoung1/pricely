from typing import List

import redis.asyncio as redis

from core.config.settings import settings
from core.logger import logger
from infrastructure.redis.message import NotificationMessage


class NotificationPublisher:
    '''
    Публикует уведомления в Redis очередь.

    Используется чекером для отправки уведомлений боту.
    '''

    def __init__(self, redis_client: redis.Redis | None = None):
        self._redis = redis_client
        self._queue_name = settings.REDIS_QUEUE_NAME

    async def connect(self) -> None:
        '''Подключиться к Redis'''
        if self._redis is None:
            self._redis = redis.from_url(settings.redis_url)
        logger.info('Publisher подключен к Redis')

    async def close(self) -> None:
        '''Закрыть соединение'''
        if self._redis:
            await self._redis.close()
            logger.info('Publisher отключен от Redis')

    async def publish(self, message: NotificationMessage) -> None:
        '''Опубликовать одно уведомление'''
        await self._redis.lpush(self._queue_name, message.model_dump_json())
        logger.debug(f'Уведомление опубликовано: chat_id={message.chat_id}')

    async def publish_many(self, messages: List[NotificationMessage]) -> int:
        '''
        Опубликовать несколько уведомлений.

        Returns:
            Количество опубликованных сообщений.
        '''
        if not messages:
            return 0

        pipe = self._redis.pipeline()
        for msg in messages:
            pipe.lpush(self._queue_name, msg.model_dump_json())
        await pipe.execute()

        logger.info(f'Опубликовано {len(messages)} уведомлений')
        return len(messages)

    async def __aenter__(self) -> 'NotificationPublisher':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
