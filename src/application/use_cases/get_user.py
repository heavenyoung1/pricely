from src.application.interfaces.repositories import UserRepository
from src.domain.entities import User
from src.domain.exceptions import UserNotFoundError


class GetUserUseCase:
    """Use case для получения данных о пользователе."""

    def __init__(self, user_repo: UserRepository):
        """
        Инициализация UseCase для получения пользователя.

        :param user_repo: Репозиторий для работы с пользователями.
        """
        self.user_repo = user_repo

    def execute(self, user_id: str) -> User:
        """
        Основной метод для выполнения логики получения пользователя.

        1. Проверяет, существует ли пользователь с таким ID в репозитории.
        2. Если пользователь существует, возвращает его данные.
        3. Если пользователь не существует, генерирует исключение.

        :param user_id: ID пользователя, которого нужно получить.
        :return: Объект пользователя.
        :raises UserNotFoundError: Если пользователь с таким ID не найден.
        """
        # 1. Получаем пользователя по ID
        user = self.user_repo.get(user_id)

        # 2. Если пользователь не найден, генерируем исключение
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")

        # 3. Возвращаем найденного пользователя
        return user
