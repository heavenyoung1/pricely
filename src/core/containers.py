from dependency_injector import containers, providers
from src.infrastructure.services import ProductService, NotificationService
from src.core import SQLAlchemyUnitOfWork
from src.presentation.bot.config import BOT_TOKEN
from aiogram import Bot

class Container(containers.DeclarativeContainer):
    # Поставщик для UnitOfWork (например, для работы с базой данных)
    uow_factory = providers.Singleton(SQLAlchemyUnitOfWork)
    
    # Поставщик для ProductService
    product_service = providers.Factory(ProductService, uow_factory=uow_factory)
    
    # Поставщик для Bot (создаем единственный экземпляр)
    bot = providers.Singleton(Bot, token=BOT_TOKEN)

    # Поставщик для NotificationService, который требует bot
    notification_service = providers.Factory(NotificationService, bot=bot)