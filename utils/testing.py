from time import sleep
from utils.webdriver import init_driver  # Замени на путь к твоей функции

driver = init_driver(headless=False)  # headless=True — если не нужен GUI
driver.get("https://www.ozon.ru/")
sleep(5)  # Просто подождать немного, чтобы визуально увидеть результат
print(driver.title)
driver.quit()