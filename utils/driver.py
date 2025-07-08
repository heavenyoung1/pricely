from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

def init_driver(headless= None, user_agent=None, proxy=None , wait_time=10):
    options = Options()

    # Базовые настройки Chrome
    if headless:
        options.add_argument("--headless") # Режим, при котором браузер работает без графического интерфейса

    options.add_argument("--no-sandbox") # Отключает песочницу (sandbox) для работы под root (например, в Docker).
    options.add_argument("--disable-gpu") # Отключает использование GPU
    options.add_argument("--disable-blink-features=AutomationControlled") # Скрывает признаки автоматизации (например, убирает флаг navigator.webdriver = true).
    options.add_argument("--start-maximized") # Запускает браузер в максимальном размере окна

    # Пользовательские настройки
    if user_agent:
        options.add_argument(f'user-agent={user_agent}') # Имитация разных устройств (ПК, мобильные)
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    # Инициализация драйвера
    driver = webdriver.Chrome(options=options)

    # Stealth-настройки (используем переданный user_agent или дефолтный)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            user_agent=user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    return driver