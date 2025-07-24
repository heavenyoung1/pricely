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
    stealth_settings = settings.SELENIUM_STEALTH_SETTINGS.copy() # Копируем, чтобы не изменять оригинал??
    stealth_settings['user_agent'] = user_agent or settings.DEFAULT_USER_AGENT

    stealth(
        driver,
        **stealth_settings,
    )

def init_driver(headless: bool = settings.SELENIUM_HEADLESS, 
                user_agent: str = settings.DEFAULT_USER_AGENT, 
                proxy: str = settings.SELENIUM_WAIT_TIME, 
                wait_time: int = settings.SELENIUM_WAIT_TIME) -> webdriver.Chrome:
    """
    Инициализирует Chrome WebDriver с поддержкой stealth-настроек.
    :return: Настроенный экземпляр WebDriver
    """
    options = Options()

    chrome_args = settings.SELENIUM_CHROME_ARGS.copy() # Копируем, чтобы не изменять оригинал
    optional_args = settings.SELENIUM_CHROME_ARGS.copy()
    optional_args = [
        "--headless=new" if headless else None,
        f"--user-agent={user_agent}" if user_agent else None,
        f"--proxy-server={proxy}" if proxy else None,
    ]
    chrome_args.extend([arg for arg in optional_args if arg is not None])
    
    for arg in chrome_args:
        options.add_argument(arg)

    driver = webdriver.Chrome(options=options)
    apply_stealth_settings(driver, user_agent)
    return driver