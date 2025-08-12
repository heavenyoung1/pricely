from src.domain.entities import User
from src.interfaces.dto import UserDTO
from src.infrastructure.database.models import ORMUser


class UserMapper:
    @staticmethod
    def dto_to_domain(dto: UserDTO) -> User:
        return User(
            id=dto.id,
            username=dto.username,
            chat_id=dto.chat_id,
            products=dto.products
        )

    @staticmethod
    def domain_to_dto(domain: User) -> UserDTO:
        return UserDTO(
            id=domain.id,
            username=domain.username,
            chat_id=domain.chat_id,
            products=domain.products
        )

    @staticmethod
    def domain_to_orm(domain: User) -> ORMUser:
        return ORMUser(
            id=domain.id,
            username=domain.username,
            chat_id=domain.chat_id,
            products=domain.products
        )

    @staticmethod
    def orm_to_domain(orm: ORMUser) -> User:
        return User(
            id=orm.id,
            username=orm.username,
            chat_id=orm.chat_id,
            products=list(orm.products) if orm.products else []
        )