from pydantic import BaseModel


class NotificationMessage(BaseModel):
    '''
    Сообщение для очереди уведомлений.

    Содержит все данные, необходимые боту для отправки уведомления.
    Бот не обращается к БД — всё уже в сообщении.
    '''

    chat_id: int
    product_name: str
    product_link: str | None
    price_with_card: int
    price_without_card: int
    previous_with_card: int
    previous_without_card: int
