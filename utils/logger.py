import logging
from typing import Optional

class CustomLogger:
    """Класс для централизованного управления логами приложения."""

    _instanse = None # Шаблон проектирования Singleton (Одиночка)

    def __new__(cls):
        if cls._instanse is None:
            cls._instanse = super(CustomLogger, cls).__new__(cls)
            cls._instanse._initialize_logger()
            return cls._instanse
    
    def _initialize_logger(self):
        """Инициализирует конфигурацию логгера."""
        self.logger = logging.getLogger("AuthServiceLogger")
        self.logger.setLevel(logging.DEBUG)  # Уровень логирования по умолчанию

        # Удаляем все существующие обработчики, чтобы избежать дублирования
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Настройка обработчика для вывода в консоль
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message: str, extra: Optional[dict] = None):
        """Логирует сообщение на уровне DEBUG."""
        self.logger.debug(message, extra=extra or {})

    def info(self, message: str, extra: Optional[dict] = None):
        """Логирует сообщение на уровне INFO."""
        self.logger.info(message, extra=extra or {})

    def warning(self, message: str, extra: Optional[dict] = None):
        """Логирует сообщение на уровне WARNING."""
        self.logger.warning(message, extra=extra or {})

    def error(self, message: str, extra: Optional[dict] = None):
        """Логирует сообщение на уровне ERROR."""
        self.logger.error(message, extra=extra or {})

    def critical(self, message: str, extra: Optional[dict] = None):
        """Логирует сообщение на уровне CRITICAL."""
        self.logger.critical(message, extra=extra or {})

# Глобальный экземпляр для удобного использования
logger = CustomLogger()