import asyncio
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from core.interfaces.product import IProductParser, ProductInfo
from core.models.market import Marketplace