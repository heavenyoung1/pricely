from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

from config.settings import settings

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
        user_agent=user_agent,
    )

def init_driver(headless: bool = settings.SELENIUM_HEADLESS, 
                user_agent: str = settings.DEFAULT_USER_AGENT, 
                proxy: str = settings.SELENIUM_WAIT_TIME, 
                wait_time: int = settings.SELENIUM_WAIT_TIME) -> webdriver.Chrome:
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
        "--log-level=3",                                  # Уровень 3 подавляет большинство сообщений
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