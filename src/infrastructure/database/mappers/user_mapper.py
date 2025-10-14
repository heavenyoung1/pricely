from deprecated import deprecated

from src.domain.entities import User
from src.application.dto import UserDTO
from src.infrastructure.database.models import ORMUser


class UserMapper:
    '''
    Маппер для преобразования между объектами User и ORMUser.

    Этот класс содержит методы для преобразования данных между различными слоями:
    - Domain
    - ORM (Object-Relational Mapping)
    '''

    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def dto_to_domain(dto: UserDTO) -> User:
        '''
        Преобразует объект UserDTO в объект User (доменная модель).

        :param dto: Объект типа UserDTO.
        :return: Объект типа User (доменная модель).
        '''
        return User(
            id=dto.id,
            username=dto.username,
            chat_id=dto.chat_id,
            products=dto.products,
        )

    @staticmethod
    @deprecated(reason='Этот метод скоро будет удален. Используйте новый метод для преобразования.')
    def domain_to_dto(domain: User) -> UserDTO:
        '''
        Преобразует объект User (доменная модель) в объект UserDTO (Data Transfer Object).

        :param domain: Объект типа User (доменная модель).
        :return: Объект типа UserDTO.
        '''
        return UserDTO(
            id=domain.id,
            username=domain.username,
            chat_id=domain.chat_id,
            products=domain.products,
        )

    @staticmethod
    def domain_to_orm(domain: User) -> ORMUser:
        '''
        Преобразует объект User (доменная модель) в объект ORMUser (ORM модель для работы с БД).

        :param domain: Объект типа User (доменная модель).
        :return: Объект типа ORMUser для сохранения в базе данных.
        '''
        return ORMUser(
            id=domain.id,
            username=domain.username,
            chat_id=domain.chat_id,
        )

    @staticmethod
    def orm_to_domain(orm: ORMUser) -> User:
        '''
        Преобразует объект ORMUser (ORM модель) в объект User (доменная модель).

        :param orm: Объект типа ORMUser.
        :return: Объект типа User (доменная модель).
        '''
        return User(
            id=orm.id,
            username=orm.username,
            chat_id=orm.chat_id,
            products=[up.product_id for up in orm.user_products] if orm.user_products else [],
        )
