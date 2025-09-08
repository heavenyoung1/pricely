import sys
from src.core.db_config import DataBaseSettings

if __name__ == "__main__":
    db = DataBaseSettings()
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print(db.get_alembic_url(use_test=True))
    else:
        print(db.get_alembic_url(use_test=False))
