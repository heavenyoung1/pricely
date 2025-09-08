import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # чтобы видеть src

from src.core.db_config import DataBaseSettings

if __name__ == "__main__":
    db = DataBaseSettings()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        url = db.get_db_url()
        # Замените postgresql:// на postgresql+psycopg2://
        url = url.replace("postgresql://", "postgresql+psycopg2://")
        print(url)
    else:
        url = db.get_db_url()
        url = url.replace("postgresql://", "postgresql+psycopg2://")
        print(url)