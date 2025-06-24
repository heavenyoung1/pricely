from utils.webdriver import driver

import asyncio
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

driver.get('https://www.ozon.ru/product/lanch-boks-850-ml-konteyner-dlya-hraneniya-edy-s-otdeleniyami-i-priborami-1549274404/?at=36tWj7gmGFywRNoLUvOLJy5tA0k5vKt95AXDkC6RJMRD')

title = driver.find_element(By.ID, '')
price = driver.find_element(By.ID, '.m8o_27 om6_27')

print(price)
