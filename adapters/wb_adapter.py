from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@dataclass
class WBAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver = None
    
    def __post_init__(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def parse_product(self, url: str) -> Product:
            self.driver.get(url)
            name_elem = self.driver.find_element(By.CSS_SELECTOR, '.product-page__title')
            main_price_elem = self.driver.find_element(By.CSS_SELECTOR, '.price-block__wallet-price red-price')
            sub_price_elem = self.driver.find_element(By.CSS_SELECTOR, '.price-block__final-price wallet')
            # Проверить и перевести цену в INT

    def _get_id(url: str) -> str:
        splitedStr = url.split("/")[-2]
        return splitedStr
    
