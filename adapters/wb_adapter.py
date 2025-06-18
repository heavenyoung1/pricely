from dataclasses import dataclass
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from adapters.interfaces import IMarketPlace
from models.product import Product

@dataclass
class WBAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver = None
    
    def __post_init__(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    @staticmethod
    def _get_id(url: str) -> str:
        ID = url.split("/")[-2]
        return ID

    def parse_product(self, url: str) -> Product:
        try:
            self.driver.get(url)
            product_ID = self._get_id(url)

            name = self.driver.find_element(By.CSS_SELECTOR, '.product-page__title').text
            price = self.driver.find_element(By.CSS_SELECTOR, '.price-block__wallet-price red-price').text
            last_updated = datetime.now()

            return Product(
                 id=product_ID,
                 url=url,
                 name=name,
                 price=price,
                 last_updated=last_updated,
            )
        except Exception as e:
            raise ValueError("Ошибка парсинга Wildberries") from e

    
