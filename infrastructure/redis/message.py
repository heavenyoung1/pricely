from pydantic import BaseModel


class PriceChangeItem(BaseModel):
    '''Один товар с изменённой ценой.'''

    product_name: str
    product_link: str | None
    price_with_card: int
    price_without_card: int
    previous_with_card: int
    previous_without_card: int


class NotificationMessage(BaseModel):
    '''
    Сообщение для очереди уведомлений.

    Содержит все данные, необходимые боту для отправки уведомления.
    Одно сообщение = один пользователь со всеми его изменёнными товарами.
    '''

    chat_id: int
    items: list[PriceChangeItem]
