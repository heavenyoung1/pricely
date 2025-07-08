from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) " 
    "Chrome/90.0.4430.212 Safari/537.36 "
)

def apply_stealth_settings(driver, user_agent: str = None) -> None:
    """
    Применяет stealth-настройки для маскировки Selenium WebDriver.
    
    :param driver: Экземпляр Selenium WebDriver
    :param user_agent: Пользовательский user-agent (если не указан — используется дефолтный)
    """

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        user_agent=user_agent or DEFAULT_USER_AGENT,
    )

def init_driver(headless: bool = False, user_agent: str = None, proxy: str = None, wait_time: int = 10) -> webdriver.Chrome:
    """
    Инициализирует Chrome WebDriver с поддержкой stealth-настроек.
    
    :param headless: Запуск без графического интерфейса
    :param user_agent: Пользовательский user-agent
    :param proxy: Прокси-сервер (http://host:port)
    :param wait_time: Зарезервировано для будущих фич
    :return: Настроенный экземпляр WebDriver
    """
    options = Options()

    # Основные аргументы
    chrome_args = [
        "--no-sandbox",                                   # Отключает песочницу (sandbox) для работы под root
        "--disable-gpu",                                  # Отключает использование GPU
        "--disable-blink-features=AutomationControlled",  # Скрывает признаки автоматизации
        "--start-maximized",                              # Запускает браузер в максимальном размере окна
    ]

    if headless:
        chrome_args.append("--headless=new")
    if user_agent:
        chrome_args.append(f"--user-agent={user_agent}")
    if proxy:
        chrome_args.append(f"--proxy-server={proxy}")
    
    for arg in chrome_args:
        options.add_argument(arg)

    driver = webdriver.Chrome(options=options)

    apply_stealth_settings(driver, user_agent)

    return driver