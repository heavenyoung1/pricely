import logging
from src.domain.entities import User
from src.application.interfaces.repositories import UserRepository

logger = logging.getLogger(__name__)

class CreateUserUseCase:
    '''
    Use case для создания пользователя.

    Этот класс отвечает за создание нового пользователя в системе, проверяя,
    существует ли уже пользователь с данным ID. Если пользователь существует,
    создание пропускается.
    '''

    def __init__(self, user_repo: UserRepository):
        '''
        Инициализация UseCase для создания пользователя.

        :param user_repo: Репозиторий для работы с пользователями.
        '''
        self.user_repo = user_repo

    def execute(self, user: User) -> None:
        '''
        Основной метод для выполнения логики создания пользователя.

        1. Проверяет, существует ли пользователь с таким ID в репозитории.
        2. Если пользователь существует, выводит информацию и пропускает создание.
        3. Если пользователь не существует, сохраняет его в репозитории.

        :param user: Объект пользователя, которого нужно создать.
        '''
        # 1. Проверяем, существует ли пользователь
        existing = self.user_repo.get(user.id)
        if existing:
            logger.info(f'Пользователь {user.id} уже существует, пропускаем создание')
            return

        # 2. Сохраняем нового пользователя
        self.user_repo.save(user)
        logger.info(f'Пользователь {user.id} успешно создан')