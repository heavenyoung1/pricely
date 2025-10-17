from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Update

class ServiceMiddleware(BaseMiddleware):
    '''Middleware для внедрения зависимостей (product_service, etc.)'''
    
    def __init__(self, product_service, notification_service=None):
        super().__init__()
        self.product_service = product_service
        self.notification_service = notification_service

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        # Добавляем сервисы в контекст данных
        data['product_service'] = self.product_service
        if self.notification_service:
            data['notification_service'] = self.notification_service
        
        return await handler(event, data)