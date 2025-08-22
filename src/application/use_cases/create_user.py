import logging
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)

class UserCreationError(Exception):
    '''Исключение для ошибок при создании пользователя.'''
    pass

class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user: User) -> None:
        try:
            existing = self.user_repo.get(user.id)
            if existing:
                raise UserCreationError(f'Пользователь {user.id} уже существует')

            self.user_repo.save(user)

        except UserCreationError:
            # не трогаем свои бизнесовые ошибки
            raise
        except Exception as e:
            logger.error(f'Ошибка при создании пользователя {user.id}: {e}')
            raise UserCreationError(f'Ошибка создания пользователя: {e}')