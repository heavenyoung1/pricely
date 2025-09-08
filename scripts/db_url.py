#!/usr/bin/env python3
import sys
import os

# Добавляем текущую директорию в Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.db_config import DataBaseSettings

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        settings = DataBaseSettings()
        if not settings.is_test_db_configured:
            print("Тестовая БД не настроена")
            sys.exit(1)
        test_settings = DataBaseSettings(NAME=settings.TEST_NAME)
        print(test_settings.get_db_url())
    else:
        settings = DataBaseSettings()
        print(settings.get_db_url())

if __name__ == "__main__":
    main()