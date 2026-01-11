import re

from src.core.logger import logger


class LinkAdapter:
    @staticmethod
    def extract_link(text: str) -> str:
        pattern = r'https?://\S+'

        match = re.search(pattern, text)

        if match:
            return match.group(0)

        logger.error(f'Ссылка в тексте не обнаружена: {text}')
        raise ValueError('Ссылка не найдена')