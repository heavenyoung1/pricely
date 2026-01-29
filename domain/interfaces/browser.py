from abc import ABC, abstractmethod
from typing import Optional
from playwright.async_api import Browser, BrowserContext, Page


class IBrowserManager(ABC):
    '''
    Интерфейс менеджера браузера
    Определяет все необходимые операции для парсинга
    '''

    @abstractmethod
    async def start(self) -> None:
        '''Запустить браузер с настройками'''
        pass

    @abstractmethod
    async def get_browser(self) -> Browser:
        '''Получить экземпляр браузера'''
        pass

    @abstractmethod
    async def get_context(self) -> BrowserContext:
        '''Получить контекст браузера'''
        pass

    @abstractmethod
    async def open_page(self, url: str) -> Page:
        '''
        Открыть новую страницу и перейти по URL

        Args:
            url: Адрес страницы для открытия

        Returns:
            Page: Объект открытой страницы
        '''
        pass

    @abstractmethod
    async def wait_for_selector(
        self, page: Page, selector: str, timeout: Optional[int] = None
    ) -> None:
        '''
        Ждать появления элемента на странице

        Args:
            page: Страница для ожидания
            selector: CSS или XPath селектор
            timeout: Таймаут ожидания в миллисекундах
        '''
        pass

    @abstractmethod
    async def close(self) -> None:
        '''Закрыть браузер и освободить ресурсы'''
        pass
