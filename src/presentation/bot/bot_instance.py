import os
from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError('BOT_TOKEN не найден в .env')

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
