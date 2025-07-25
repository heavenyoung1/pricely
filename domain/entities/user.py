from dataclasses import dataclass

@dataclass
class User:
    '''Сущность пользователь'''
    telegram_id: str
    username: str
