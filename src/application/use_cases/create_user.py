import logging
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from exceptions import UserCreationError

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user: User) -> None:
        try:
            existing = self.user_repo.get(user.id)
            if existing:
                logger.info(f'Пользователь {user.id} уже существует, пропускаем создание')
                return  # Пользователь уже существует, ничего не делаем

            self.user_repo.save(user)
            logger.info(f'Пользователь {user.id} успешно создан')

        except Exception as e:
            logger.error(f'Ошибка при создании пользователя {user.id}: {e}')
            raise UserCreationError(f'Ошибка создания пользователя: {e}')