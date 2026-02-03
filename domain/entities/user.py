from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    chat_id: str

    @staticmethod
    def create(
        *,
        username: str,
        chat_id: str,
    ) -> 'User':
        return User(
            id=None,
            username=username,
            chat_id=chat_id,
        )
