from selenium import webdriver
from selenium.webdriver.common.by import By
from functools import wraps


# Декоратор для логирования и обработки ошибок
def with_engine(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        driver = webdriver.Chrome()   # Можно заменить на Firefox() или др.
        try:
            result = func(driver, *args, **kwargs)
            return result
        except Exception as e:
            print(f"[Ошибка] {e}")
        finally:
            driver.quit()
    return wrapper