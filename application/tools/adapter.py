import re
from core.logger import logger


class LinkAdapter:

    @staticmethod
    async def is_url(text):
        '''Проверяет, начинается ли строка с https://'''
        pattern = r'^https?://'
        return bool(re.match(pattern, text))

    @classmethod
    async def exctract_link(cls, text: str) -> str:
        '''
        Проверяет, является ли переданный текст ссылкой на Ozon. Если это не ссылка,
        извлекает ссылку из текста.

        :param input_str: Строка, которая может быть ссылкой или содержать ссылку.
        :return: Ссылка на товар на Ozon.
        :raises ValueError: Если в строке не найдено валидной ссылки на Ozon.
        '''
        if await cls.is_url(text):
            return text

        listing = text.split()
        url = listing[-1]
        return url
