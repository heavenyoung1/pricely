import logging
import os
from pathlib import Path

logger = logging.getLogger("Bloom")
logger.setLevel(logging.DEBUG)

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# Добавление консольного обработчика
logger.addHandler(console_handler)

# Файловый обработчик (только если есть права на запись)
try:
    # Пытаемся использовать директорию logs, если она существует
    log_dir = Path("/app/logs")
    if log_dir.exists() and os.access(log_dir, os.W_OK):
        log_file = log_dir / "app.log"
    else:
        # Иначе пытаемся использовать текущую директорию
        log_file = Path("app.log")
        # Создаем файл, если его нет, для проверки прав
        log_file.touch(exist_ok=True)
        log_file.unlink()  # Удаляем тестовый файл

    file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)
except (PermissionError, OSError):
    # Если нет прав на запись, используем только консольный handler
    pass
