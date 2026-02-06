from dataclasses import fields as dataclass_fields
from typing import Optional, List

from domain.entities.user_products import ParsedProduct, CheckedPrice
from domain.entities.product_fields import (
    ProductFieldsForAdd,
    ProductFieldsForCheck,
)
from application.interfaces.browser import IBrowserManager
from application.interfaces.parser import IProductParser
from core.logger import logger


class ProductParser(IProductParser):
    '''Парсер товаров для извлечения данных со страниц магазина.'''

    def __init__(
        self,
        browser: IBrowserManager,
        fields_for_add: ProductFieldsForAdd,
        fields_for_check: ProductFieldsForCheck,
    ) -> None:
        '''
        Инициализирует парсер товаров.

        Args:
            browser: Менеджер браузера для открытия страниц.
            fields_for_add: XPath-селекторы полей для добавления нового товара.
            fields_for_check: XPath-селекторы полей для проверки цен.
        '''
        self.browser = browser
        self.fields_for_add = fields_for_add
        self.fields_for_check = fields_for_check

    async def parse_new_product(
        self,
        url: str,
    ) -> ParsedProduct:
        '''
        Парсит страницу товара для добавления в систему.

        Извлекает полную информацию о товаре: артикул, название и цены.
        Используется при первичном добавлении товара в отслеживание.

        Args:
            url: URL страницы товара.

        Returns:
            ParsedProduct с данными о товаре.
        '''
        page = await self.browser.open_page(url)

        parsed_data = {}
        for field in dataclass_fields(self.fields_for_add):
            xpath = getattr(self.fields_for_add, field.name)
            text = await self._extract_text(page, xpath)
            logger.debug(f'[PARSER] Поле {field.name}: xpath={xpath}, text={text}')
            if field.name == 'article':
                parsed_data[field.name] = self._extract_article(text)
            elif field.name == 'name':
                parsed_data[field.name] = text
            else:
                parsed_data[field.name] = self._clean_price(text)

        # Сохраняем скриншот для отладки если name не найден
        if not parsed_data.get('name'):
            try:
                await page.screenshot(path='/app/debug_screenshot.png', full_page=True)
                logger.warning('[PARSER] Товар не найден! Скриншот: /app/debug_screenshot.png')
            except Exception as e:
                logger.warning(f'[PARSER] Не удалось сохранить скриншот: {e}')

        await page.close()

        parsed_product = ParsedProduct.create(
            article=parsed_data['article'],
            name=parsed_data['name'],
            link=url,
            price_with_card=parsed_data['price_with_card'],
            price_without_card=parsed_data['price_without_card'],
        )
        logger.info(f'Спарсен новый товар: {url}')
        return parsed_product

    async def fetch_current_prices(
        self,
        urls: List[str],
    ) -> List[CheckedPrice]:
        '''
        Парсит текущие цены для списка товаров.

        Извлекает только ценовую информацию (без артикула и названия).
        Используется для периодической проверки изменения цен.

        Args:
            urls: Список URL страниц товаров для проверки.

        Returns:
            Список CheckedPrice с актуальными ценами.
        '''
        results = []
        for url in urls:
            page = await self.browser.open_page(url)

            parsed_data = {}
            for field in dataclass_fields(self.fields_for_check):
                xpath = getattr(self.fields_for_check, field.name)
                text = await self._extract_text(page, xpath)
                parsed_data[field.name] = self._clean_price(text)

            await page.close()

            checked_price = CheckedPrice.create(
                url=url,
                price_with_card=parsed_data['price_with_card'],
                price_without_card=parsed_data['price_without_card'],
            )
            results.append(checked_price)
            logger.info(f'Проверена цена: {url}')

        return results

    async def _extract_text(self, page, xpath: str) -> Optional[str]:
        '''
        Извлекает текстовое содержимое элемента по XPath-селектору.

        Args:
            page: Объект страницы Playwright.
            xpath: XPath-селектор элемента.

        Returns:
            Текст элемента или None, если элемент не найден.
        '''
        try:
            locator = page.locator(xpath)
            text = await locator.first.text_content(timeout=5000)
            return text.strip() if text else None
        except Exception:
            return None

    @staticmethod
    def _extract_article(text: Optional[str]) -> Optional[str]:
        '''
        Извлекает артикул из текста.

        Args:
            text: Строка с артикулом (например, 'Артикул: 1287151806').

        Returns:
            Артикул как строка или None, если текст пустой.
        '''
        if not text:
            return None
        digits = ''.join(c for c in text if c.isdigit())
        return digits if digits else None

    @staticmethod
    def _clean_price(text: Optional[str]) -> Optional[int]:
        '''
        Очищает строку цены и преобразует в целое число.

        Удаляет все нецифровые символы (пробелы, валюту, разделители).

        Args:
            text: Строка с ценой (например, '1 299 ₽').

        Returns:
            Цена как целое число или None, если текст пустой.
        '''
        if not text:
            return None
        digits = ''.join(c for c in text if c.isdigit())
        return int(digits) if digits else None
