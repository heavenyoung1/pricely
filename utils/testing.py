from engine.session_engine import SessionEngine
import time

with SessionEngine() as session:
    session.navigate("https://www.ozon.ru/")
    print("Cookies:", session.get_cookies())
    print("Headers:", session.get_headers())
    time.sleep(5)
    print("Title:", session.driver.title)
    session.refresh_session("https://www.ozon.ru/")  # Обновляем сессию
    print("New Cookies:", session.get_cookies())