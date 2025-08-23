from .webdriver import with_engine
from selenium.webdriver.common.by import By

# Функция с использованием XPath
@with_engine
def get(driver, url: str, xpath: str):
    driver.get(url)
    element = driver.find_element(By.XPATH, xpath)
    return element.text

# === Пример использования ===
if __name__ == "__main__":
    text = get("https://www.ozon.ru/product/dzhinsy-befree-883110146/", "//h1")
    print("Найденный текст:", text)