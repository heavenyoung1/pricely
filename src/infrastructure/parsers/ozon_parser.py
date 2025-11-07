from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .session_decorator import session_engine_decorator as session_wrapper
from .session_engine import SessionEngine
from typing import Dict, List, Optional
import logging
import sys

from src.infrastructure.parsers.interfaces import Parser
from src.domain.exceptions import ParserProductError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ozon_parser.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class OzonParser(Parser):
    """Парсер товаров с Ozon. Реализует парсинг данных о товаре с маркетплейса Ozon."""

    @session_wrapper(headless=True)
    def parse_product(self, session: SessionEngine, url: str) -> Dict:
        """Парсит страницу товара по URL и возвращает данные о товаре.

        :param url: URL страницы товара.
        :return: Словарь с данными о товаре (ID, название, цена, рейтинг и т.д.)
        :raises ParserError: В случае ошибки парсинга.
        """
        try:
            session.navigate(url)
            logger.info(f"Загружена страница: {url}")
            parsed_data = {
                "id": self._extract_id(session),
                "name": self._extract_name(session),
                "price_with_card": self._extract_price_with_card(session),
                "price_without_card": self._extract_price_without_card(session),
            }
            # Если не удалось извлечь критически важные данные, выбрасываем ошибку
            if not parsed_data["id"] or not parsed_data["name"]:
                raise ParserProductError(
                    f"Не удалось извлечь необходимые данные с страницы: {url}"
                )

            logger.info(f"Данные, полученные парсером: {parsed_data}")
            return parsed_data

        except ParserProductError as e:
            logger.error(f"Ошибка парсинга страницы {url}: {e}")
            raise  # Выбрасываем наше специфичное исключение
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            raise ParserProductError(f"Ошибка парсинга товара по ссылке: {url}")

    @session_wrapper(headless=True)
    def check_product(self, session: SessionEngine, url: str) -> Dict:
        """Парсит страницу товара по URL и возвращает данные о товаре.

        :param url: URL страницы товара.
        :return: Словарь с актуальными ценами товара
        :raises ParserError: В случае ошибки парсинга.
        """
        try:
            session.navigate(url)
            logger.info(f"Загружена страница: {url}")
            parsed_data = {
                "price_with_card": self._extract_price_with_card(session),
                "price_without_card": self._extract_price_without_card(session),
            }
            logger.info(f"Данные, полученные парсером: {parsed_data}")
            return parsed_data
        except Exception as e:
            logger.error(f"Ошибка при парсинге страницы {url}: {e}")
            raise

    # ----------------- Вспомогательные методы -----------------

    def _extract_digits(self, text: str) -> int:
        """Извлекает только цифры из строки.

        :param text: Строка с цифрами.
        :return: Цифры в виде целого числа.
        """
        return int("".join(ch for ch in text if ch.isdigit()))

    def _extract_id(self, session: SessionEngine) -> str:
        """Извлекает артикул товара из страницы.

        :param session: Экземпляр сессии.
        :return: Артикул товара.
        """
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(text(),'Артикул')]")
                )
            )
            text = session._extract_text(element_obj)
            article = self._extract_digits(text)
            logger.info(f"Найден артикул: {article}")
            return str(article)
        except Exception as e:
            logger.error(f"Ошибка при извлечении артикула: {e}")
            return None

    def _extract_name(self, session: SessionEngine) -> str:
        """Извлекает название товара.

        :param session: Экземпляр сессии.
        :return: Название товара.
        """
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@data-widget='webProductHeading']//h1")
                )
            )
            name = session._extract_text(element_obj)
            logger.info(f"Найдено название товара: {name}")
            return name
        except Exception as e:
            logger.error(f"Ошибка при извлечении названия товара: {e}")
            return None

    def _extract_price_with_card(self, session: SessionEngine) -> Optional[int]:
        """Извлекает цену товара с картой.

        :param session: Экземпляр сессии.
        :return: Цена с картой.
        """
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//span[@class='tsHeadline600Large']")
                )
            )
            text = session._extract_text(element_obj)
            price = self._extract_digits(text)
            logger.info(f"Найдена цена с картой: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены с картой: {e}")
            return None

    def _extract_price_without_card(self, session: SessionEngine) -> Optional[int]:
        """Извлекает цену товара без карты.

        :param session: Экземпляр сессии.
        :return: Цена без карты.
        """
        try:
            element_obj = WebDriverWait(session.driver, session.wait_time).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//span[contains(text(),'₽') and contains(@class,'tsHeadline500Medium')]",
                    )
                )
            )
            text = session._extract_text(element_obj)
            price = self._extract_digits(text)
            logger.info(f"Найдена цена без карты: {price}")
            return price
        except Exception as e:
            logger.error(f"Ошибка при извлечении цены без карты: {e}")
            return None