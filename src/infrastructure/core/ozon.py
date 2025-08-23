from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .webdriver import with_engine

class OzonParser:

    @with_engine
    def parse_name(driver, url: str) -> str:
        driver.get(url)
        el = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
        )
        return el.text.strip()
    
url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"

name = OzonParser.parse_name(url)
print("Название:", name)