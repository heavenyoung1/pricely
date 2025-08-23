from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
import logging
from config import DEFAULT_USER_AGENT, DEFAULT_STEALTH_CONFIG, DriverConfig, StealthConfig

logger = logging.getLogger(__name__)

class BrowserEngine:
    """Движок для управления Chrome WebDriver с stealth-настройками"""
    
    def __init__(self, config: Optional[DriverConfig] = None, 
                 stealth_config: Optional[StealthConfig] = None):
        self.config = config or DriverConfig()
        self.stealth_config = stealth_config or DEFAULT_STEALTH_CONFIG
        self.driver = None
        
    def apply_stealth_settings(self, driver: webdriver.Chrome, 
                             user_agent: Optional[str] = None) -> None:
        """
        Применяет stealth-настройки для маскировки Selenium WebDriver.
        
        :param driver: Экземпляр Selenium WebDriver
        :param user_agent: Пользовательский user-agent
        """
        try:
            stealth(
                driver,
                languages=self.stealth_config.languages,
                vendor=self.stealth_config.vendor,
                platform=self.stealth_config.platform,
                webgl_vendor=self.stealth_config.webgl_vendor,
                renderer=self.stealth_config.renderer,
                fix_hairline=self.stealth_config.fix_hairline,
                user_agent=user_agent or self.config.user_agent or DEFAULT_USER_AGENT,
            )
            logger.info("Stealth settings applied successfully")
            
        except Exception as e:
            logger.error(f"Failed to apply stealth settings: {e}")
            raise
    
    def _setup_chrome_options(self) -> Options:
        """Настраивает опции Chrome"""
        options = Options()
        
        # Базовые аргументы
        chrome_args = [
            "--no-sandbox",           # Отключает песочницу
            "--disable-gpu",          # Отключает использование GPU
            "--disable-blink-features=AutomationControlled",  # Скрывает автоматизацию
            "--start-maximized",      # Максимальный размер окна
            f"--window-size={self.config.window_size[0]},{self.config.window_size[1]}",
        ]
        
        # Дополнительные настройки
        if self.config.headless:
            chrome_args.append("--headless=new")
        
        if self.config.user_agent:
            chrome_args.append(f"--user-agent={self.config.user_agent}")
        
        if self.config.proxy:
            chrome_args.append(f"--proxy-server={self.config.proxy}")
        
        if self.config.disable_images:
            chrome_args.extend([
                "--blink-settings=imagesEnabled=false",
                "--disable-images"
            ])
        
        if self.config.disable_javascript:
            chrome_args.append("--disable-javascript")
        
        # Экспериментальные опции для обхода детекции
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Добавляем все аргументы
        for arg in chrome_args:
            options.add_argument(arg)
            
        return options
    
    def init_driver(self) -> webdriver.Chrome:
        """
        Инициализирует Chrome WebDriver с поддержкой stealth-настроек.
        
        :return: Настроенный экземпляр WebDriver
        """
        try:
            logger.info("Initializing Chrome WebDriver...")
            
            # Настраиваем опции
            options = self._setup_chrome_options()
            
            # Создаем драйвер
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Применяем stealth-настройки
            self.apply_stealth_settings(self.driver)
            
            # Устанавливаем таймауты
            self.driver.implicitly_wait(self.config.wait_time)
            
            logger.info("WebDriver initialized successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def quit(self) -> None:
        """Завершает работу драйвера"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver terminated")
    
    def __enter__(self):
        """Контекстный менеджер"""
        self.init_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Завершение контекста"""
        self.quit()