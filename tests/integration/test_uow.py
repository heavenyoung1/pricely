# import pytest
# from sqlalchemy import text

# from src.core.db_connection import DatabaseConnection, DataBaseSettings
# from src.core import SQLAlchemyUnitOfWork


# @pytest.mark.integration
# def test_uow_initialization():
#     """
#     Проверяет, что UnitOfWork корректно инициализируется и поднимает репозитории.
#     """
#     with SQLAlchemyUnitOfWork() as uow:
#         assert uow._session is not None
#         assert uow.products is not None
#         assert uow.prices is not None
#         assert uow.users is not None


# @pytest.mark.integration
# def test_uow_commit_creates_data():
#     """
#     Проверяет, что commit сохраняет данные в БД.
#     Для теста используем временную вставку через raw SQL.
#     """
#     with SQLAlchemyUnitOfWork() as uow:
#         uow._session.execute(text("CREATE TEMP TABLE test_table (id SERIAL PRIMARY KEY, name TEXT)"))
#         uow._session.execute(text("INSERT INTO test_table (name) VALUES ('test1')"))
#         uow.commit()

#         # Проверяем, что данные сохранились
#         result = uow._session.execute(text("SELECT name FROM test_table")).scalar()
#         assert result == "test1"


# @pytest.mark.integration
# def test_uow_rollback_discards_data():
#     """
#     Проверяет, что rollback отменяет изменения.
#     """
#     with SQLAlchemyUnitOfWork() as uow:
#         uow._session.execute(text("CREATE TEMP TABLE test_table2 (id SERIAL PRIMARY KEY, name TEXT)"))
#         uow._session.execute(text("INSERT INTO test_table2 (name) VALUES ('rollback_test')"))
#         uow.rollback()

#         # Должно быть пусто, так как откатили
#         result = uow._session.execute(text("SELECT name FROM test_table2")).first()
#         assert result is None
