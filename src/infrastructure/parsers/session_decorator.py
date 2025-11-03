from functools import wraps
from .session_engine import SessionEngine
import logging
from typing import Callable, Optional

logger = logging.getLogger(__name__)


def session_engine_decorator(
    headless: bool = False,
    user_agent: Optional[str] = None,
    proxy: Optional[str] = None,
    wait_time: int = 10,
) -> Callable:
    """
    Декоратор для управления сессией WebDriver с использованием SessionEngine.

    Создает и настраивает экземпляр SessionEngine, передает его в декорируемую функцию,
    а после выполнения (успешного или с ошибкой) закрывает WebDriver.

    Args:
        headless (bool): Запуск браузера в headless-режиме (без GUI).
        user_agent (str, optional): Пользовательский user-agent.
        proxy (str, optional): Прокси-сервер в формате http://host:port.
        wait_time (int): Время ожидания для загрузки страниц (сек).

    Returns:
        Callable: Обернутая функция, управляющая сессией WebDriver.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            session = None
            try:
                # Создаем объект сессии WebDriver
                session = SessionEngine(
                    headless=headless,
                    user_agent=user_agent,
                    proxy=proxy,
                    wait_time=wait_time,
                )
                result = func(self, session, *args, **kwargs)
                return result
            except Exception as e:
                # Логируем ошибку, если она произошла в процессе выполнения функции
                logger.error(f"Ошибка в декорируемой функции: {e}")
                raise
            finally:
                # Закрытие сессии WebDriver в любом случае
                if session:
                    session.quit()

        return wrapper

    return decorator
