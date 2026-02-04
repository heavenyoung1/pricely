from infrastructure.database.unit_of_work import UnitOfWorkFactory
from domain.entities.user import User
from core.logger import logger
from domain.exceptions import UserCreateError


class CreateUserUseCase:
    '''Use case для создания нового пользователя в системе.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, user_create: User) -> User:
        '''
        Создаёт и сохраняет нового пользователя в БД.

        Args:
            user_create: Данные пользователя (username, chat_id).

        Returns:
            Созданный и сохранённый пользователь.

        Raises:
            UserCreateError: При ошибке создания пользователя.
        '''
        async with self.uow_factory.create() as uow:
            try:
                user = User.create(
                    username=user_create.username,
                    chat_id=user_create.chat_id,
                )

                save_user = await uow.user_repo.save(user)

                logger.info(f'Пользователь {save_user.username} сохранен в БД')

                return save_user

            except UserCreateError as e:
                logger.error(f'Ошибка при создании пользователя: {e}')
                raise UserCreateError(user.id)
