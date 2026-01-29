from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    chat_id: str

    @staticmethod
    def create(
        *,
        name: str,
        chat_id: str,
    ) -> 'User':
        return User(
            id=None,
            name=name,
            chat_id=chat_id,
        )
