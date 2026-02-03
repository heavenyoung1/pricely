from dataclasses import fields as dataclass_fields
from typing import Optional, List

from domain.entities.user_products import UserProductsData, CheckedProduct
from domain.entities.product_fields import (
    ProductFieldsForAdd, 
    ProductFieldsForCheck,
)
from domain.interfaces.browser import IBrowserManager
from core.logger import logger


class ProductParser():
    def __init__(
            self,
            browser: IBrowserManager,
            fiels_for_add: ProductFieldsForAdd,
            fields_for_check: ProductFieldsForCheck,
            ) -> None:
        self.browser = browser
        self.fiels_for_add = fiels_for_add
        self.fields_for_check = fields_for_check

    async def check_parse(
            self,
            data: List[str]
    ) -> List[CheckedProduct]:
        results = []
        for url in data:
            page = await self.browser.open_page(url)

            # Собираем данные в словарь
            parsed_data = {}
            for field in dataclass_fields(self.fields_for_check):
                xpath = getattr(self.fields_for_check, field.name)
                text = await self._extract_text(page, xpath)
                parsed_data[field.name] = self._clean_price(text)

            parsed_product = CheckedProduct.create(
                url=url,
                price_with_card=parsed_data['price_with_card'],
                price_without_card=parsed_data['price_without_card'],
            )
            results.append(parsed_product)
            logger.info(f"Проверена цена: {url}")

        return results

    async def _extract_text(self, page, xpath: str) -> Optional[str]:
        try:
            locator = page.locator(xpath)
            text = await locator.first.text_content(timeout=5000)
            return text.strip() if text else None
        except Exception:
            return None

    @staticmethod
    def _clean_price(text: Optional[str]) -> Optional[int]:
        if not text:
            return None
        digits = ''.join(c for c in text if c.isdigit())
        return int(digits) if digits else None
