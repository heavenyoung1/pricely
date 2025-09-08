import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # чтобы видеть src

from src.core.db_config import DataBaseSettings

if __name__ == "__main__":
    db = DataBaseSettings()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print(db.get_alembic_url(use_test=True))
    else:
        print(db.get_alembic_url(use_test=False))
