import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from core.interfaces.notifier import INotifier

class TelegramNotifier(INotifier):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify(self, user, message) -> None:
        await self.bot.send_message(chat_id=user.telegram_id, text=message)