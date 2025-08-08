from src.domain.entities import User
from src.infrastructure.database.models import ORMUser

class UserMapper:
    @staticmethod
    def to_orm(entity: User) -> ORMUser:
        return ORMUser(
        id=entity.id,
        username=entity.username,
        chat_id=entity.chat_id,
        )
        # связь products задаём через ORM

    @staticmethod
    def to_domain(model: ORMUser) -> User:
        return User(
            id=model.id,
            username=model.username,
            chat_id=model.chat_id,
            products=[product.id for product in model.products]
        )