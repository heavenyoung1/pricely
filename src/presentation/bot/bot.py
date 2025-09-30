from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import asyncio
from src.presentation.bot.config import BOT_TOKEN
from src .infrastructure.services.logger import logger
dp = Dispatcher()

# Подключаем обработчики
from .handlers.start import command_start_handler

dp.message.register(command_start_handler, CommandStart())

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Бот запущен')
    asyncio.run(main())