from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class TelegramBotSetting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    TOKEN: str = Field(..., alias="TOKEN_BOT")

bot_setting = TelegramBotSetting()