# 📉 Pricely

[Пользователь] → [TelegramBot] → [ProductService] → [Repositories] → [ORM/Models] → [Database]
    ↑              ↑                  ↑                  ↑              ↑             ↑
    |              |                  |                  |              |             |
  Ответ         Создаёт            Вызывает         Преобразуют      Генерируют    Сохраняют
                сущности          репозитории       в ORM            SQL-запросы   данные