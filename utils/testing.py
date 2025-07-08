from time import sleep
from engine.driver_factory import init_driver  # Замени на путь к твоей функции

driver = init_driver()
driver.get("https://www.ozon.ru/")
sleep(5)
print(driver.title)
driver.quit()