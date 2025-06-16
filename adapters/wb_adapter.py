from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime

@dataclass
class WBAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver = None
    
    def __post_init__(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def _get_id(url: str) -> str:
        ID = url.split("/")[-2]
        return ID

    def parse_product(self, url: str) -> Product:
            self.driver.get(url)
            product_ID = self._get_id(url)
            name = self.driver.find_element(By.CSS_SELECTOR, '.product-page__title')
            price = self.driver.find_element(By.CSS_SELECTOR, '.price-block__wallet-price red-price')
            last_updated = datetime.now()
            # Проверить и перевести цену в INT
            return Product(
                 id=product_ID,
                 url=url,
                 name=name,
                 price=price,
                 last_updated=last_updated,
            )
    
wb = WBAdapter()

    
