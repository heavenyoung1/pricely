from .test_session import SessionEngine  # импортируй свой класс
import time
import traceback

# Создаём объект движка
engine = SessionEngine(
    headless=False,
    #proxy="http://XXS6gZ:juD8L88von@141.98.132.64:3000",  # твой прокси
    #proxy=,  # твой прокси
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    wait_time=10,
)

# Проверим IP
try:
    #engine.navigate("https://httpbin.org/ip")
    engine.navigate("https://www.ozon.ru/product/krossovki-reebok-glide-dmx-1615856937/?at=46tRg56M5SZ0vxKoS6PDG0BiY7ZNM5S2DX8nATvgExAz&sh=5GPvD1YKxQ")
    
    page_source = engine.driver.page_source  # Получаем исходный код страницы
    print(page_source)  # Выведет IP (должен быть прокси IP)
except Exception as e:
    print(f"Произошла ошибка при попытке сделать запрос через прокси: {e}")
    print("Трассировка ошибки:", traceback.format_exc())

# Задержка, чтобы остаться на странице и подождать её загрузки
time.sleep(5)  # Задержка на 5 секунд

# Проверим, загрузилась ли страница
print(engine.driver.title)

# Закрытие драйвера
engine.quit()
