from src.domain.enttities.user import User
from src.infrastructure.database.models.user import ORMUser


class UserMapper:
    @staticmethod
    def to_orm(domain: User) -> "ORMUser":
        return ORMUser(
            id=domain.id if domain.id else None,
            name=domain.username,
            chat_id=domain.chat_id,
        )

    @staticmethod
    def to_domain(orm: ORMUser) -> "User":
        return User(
            id=orm.id,
            username=orm.name,
            chat_id=orm.chat_id,
        )
