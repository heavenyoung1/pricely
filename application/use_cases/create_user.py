from infrastructure.database.unit_of_work import UnitOfWorkFactory
from domain.entities.user import User
from core.logger import logger
from domain.exceptions import UserCreateError


class CreateUserUseCase:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, user_create: User):
        async with self.uow_factory.create() as uow:
            try:
                user = User.create(
                    name=user_create.username,
                    chat_id=user_create.chat_id,
                )

                save_user = await uow.user_repo.save(user)

                logger.info(f'Пользователь {save_user.username} сохранен в БД')

                return save_user

            except UserCreateError as e:
                logger.error(f'Ошибка при создании пользователя: {e}')
                raise UserCreateError(user.id)
