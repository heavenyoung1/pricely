from typing import Optional
from abc import ABC, abstractmethod

class BaseIDParser(ABC):
    """ Абстрактный класс для парсинга ID товаров из разных маркетплейсов """

    @classmethod
    @abstractmethod
    def extract_product_id(cls, url: str) -> str:
        """ Извлекает ID товара из URL """
        pass


def extract_product_id(url: str) -> str:
    splitedStr = url.split("/")[-2]
    ID = splitedStr[-10:]
    return ID

print(extract_product_id("https://www.ozon.ru/product/nabor-kvadratnyh-konteynerov-dlya-edy-i-hraneniya-fusion-6-sht-2082762097/?campaignId=543"))

def get_ID(product_id: str) -> Optional[str]:
    if not (product_id.isdigit() and len(product_id) == 10):
        raise ValueError(f"Invalid product ID - must be exactly 10 digits, got {product_id}")
    return product_id