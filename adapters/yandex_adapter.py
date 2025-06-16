from dataclasses import dataclass
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from adapters.interfaces import IMarketPlace
from models.product import Product

@dataclass
class YandexAdapter(IMarketPlace):
    driver_path: str
    driver: webdriver = None

    def __post_init__(self):
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)

    def _get_id(url: str) -> str:
        parts = url.split("/")
        id_with_params = parts[5] 
        ID = id_with_params.split("?")[0]
        return ID