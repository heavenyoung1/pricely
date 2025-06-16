from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@dataclass
class OzonAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver = None

    def __post_init__(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    @staticmethod
    def _get_id(url: str) -> str:
        splitedStr = url.split("/")[-2]
        ID = splitedStr[-10:]
        return ID

    def parse_product(self, url: str) -> Product:
        self.driver.get(url)
        try:
            name_elem = WebDriverWait(self.driver, 10000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.m8p_27.tsHeadline550Medium'))
            )
            return name_elem.text
        except Exception as e:
            print(f"Ошибка при ожидании элемента: {e}")
            return None

ozon = OzonAdapter(driver_path='C:\\Users\\Mefyod-EA\\Documents\\my_projects\\chromedriver.exe')
print(ozon.parse_product('https://www.ozon.ru/product/nabor-kvadratnyh-konteynerov-dlya-edy-i-hraneniya-fusion-6-sht-2082762097/?campaignId=543'))