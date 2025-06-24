from utils.webdriver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver.get('https://www.ozon.ru/product/lanch-boks-850-ml-konteyner-dlya-hraneniya-edy-s-otdeleniyami-i-priborami-1549274404/')

price = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.m8o_27.om6_27'))
)

print("Цена:", price.text)


