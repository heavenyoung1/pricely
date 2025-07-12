from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# Telegram
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")