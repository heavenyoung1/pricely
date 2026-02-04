# Используем официальный образ Playwright с Python
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем uv и зависимости
RUN pip install uv && \
    uv sync --frozen --no-dev

# Устанавливаем браузеры Playwright
RUN uv run playwright install chromium

# Копируем исходный код
COPY . .

# По умолчанию запускаем бота
CMD ["uv", "run", "python", "-m", "presentation.telegram.bot"]
