from dataclasses import fields as dataclass_fields
from typing import Optional, List, Dict, Any

from domain.entities.user_products import UserProductsData
from domain.entities.product_fields import ProductFields
from domain.interfaces.browser import IBrowserManager
from core.logger import logger


class ProductParser():
    def __init__(
            self,
            browser: IBrowserManager,
            fields: ProductFields,
            ) -> None:
        self.browser = browser
        self.fields = fields

    async def parse(
            self,
            data: List[str]
    ) -> List[Dict[str, Any]]:
        results = []

        for url in data.product_links:
            page = await self.browser.open_page(url)
            try:
                parsed = {
                    'chat_id': data.chat_id,
                    'url': url,
                }

                for field in dataclass_fields(self.fields):
                    xpath = getattr(self.fields, field.name)
                    text = await self._extract_text(page, xpath)

                    if field.name in ('price_with_card', 'price_without_card'):
                        parsed[field.name] = self._clean_price(text)
                    else:
                        parsed[field.name] = text

                results.append(parsed)
            except Exception as e:
                logger.error(f'Ошибка при парсинге {url}: {e}')
            finally:
                await page.close()

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
