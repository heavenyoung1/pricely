import logging
from typing import Optional
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)

class ParserUtils:
    @staticmethod
    def extract_text(element: Optional[WebElement]) -> str:
        '''Вспомогательный метод для извлечения текста элемента'''
        text = element.text.strip() if element else ""
        logger.debug(f"Извлечен текст: {text}")
        return text
    
    @staticmethod
    def extract_number(text: str) -> int:
        '''Извлекает число из текста'''
        if not text or text == "N/A":
            logger.debug("Текст пустой или 'N/A', возвращаем 0")
            return 0
        number = int("".join(filter(str.isdigit, text)))
        logger.debug(f"Извлечено число: {number}")
        return number
    
    @staticmethod
    def extract_rating(text: str) -> float:
        '''Извлекает рейтинг из текста'''
        if not text or text == "N/A":
            logger.debug("Текст пустой или 'N/A', возвращаем 0.0")
            return 0.0
        rating = float(text.split("•")[0].strip()) if "•" in text else 0.0
        logger.debug(f"Извлечен рейтинг: {rating}")
        return rating
    
    @staticmethod
    def extract_image_url(element: Optional[WebElement]) -> str:
        '''Извлекает URL изображения из элемента'''
        if element:
            try:
                img_element = element.find_element(by="tag name", value="img")
                url = img_element.get_attribute("src") or "N/A"
                logger.debug(f"Извлечен URL изображения: {url}")
                return url
            except Exception:
                pass
        logger.debug("Не удалось извлечь URL изображения, возвращаем 'N/A'")
        return "N/A"