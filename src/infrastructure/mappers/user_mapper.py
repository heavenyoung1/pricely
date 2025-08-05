from typing import TYPE_CHECKING
from src.infrastructure.database.models import ORMUser

if TYPE_CHECKING:
    from src.domain.entities import User

class UserMapper:
    @staticmethod
    def to_orm(user: User) -> ORMUser:
        '''Преобразовать User в ORMUser'''
        return ORMUser(
            user_ud=user.user_id,
            username=user.username,
            chat_id=user.chat_id,
            product=user.products #НУ ТУТ ТОЧНО НЕ ТАК!!!
        )