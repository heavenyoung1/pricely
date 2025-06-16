from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime

@dataclass
class OzonAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver.Chrome = None

    def __post_init__(self):
        self.driver = webdriver.Chrome(self.driver_path)

    @staticmethod
    def extract_product_id(url: str) -> str:
        splitedStr = url.split("/")[-2]
        ID = splitedStr[-10:]
        return ID

    def parse_product(url: str) -> Product:
        pass