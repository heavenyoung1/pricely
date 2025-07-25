from abc import ABC, abstractmethod
from typing import List, Optional

class Browser(ABC):
    """Интерфейс для работы с браузером."""
    
    @abstractmethod
    def open_page(self, url: str) -> None:
        pass
    
    @abstractmethod
    def find_element(self, by: str, value: str) -> Optional[object]:
        pass
    
    @abstractmethod
    def find_elements(self, by: str, value: str) -> List[object]:
        pass
    
    @abstractmethod
    def close(self) -> None:
        pass