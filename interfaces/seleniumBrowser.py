from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Optional

from adapters.selenium_adapter import SessionEngine

class SeleniumBrowser():
    """Реализация интерфейса Browser с использованием Selenium."""
    
    def __init__(self, headless: bool = True, user_agent: str = None, proxy: str = None, wait_time: int = 10):
        self.session = SessionEngine(
                                    headless=headless, 
                                    user_agent=user_agent, 
                                    proxy=proxy, 
                                    wait_time=wait_time,
            )
    
    def open_page(self, url: str) -> None:
        self.session.open_page(url)
    
    def find_element(self, by: str, value: str) -> Optional[object]:
        try:
            return self.session.find_element(by, value)
        except Exception:
            return None
    
    def find_elements(self, by: str, value: str) -> List[object]:
        try:
            return self.session.driver.find_elements(by=by, value=value)
        except Exception:
            return []
    
    def close(self) -> None:
        self.session.close()