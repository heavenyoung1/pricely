from domain.entities.price import Price

from dataclasses import dataclass


@dataclass
class Notification:
    user_id: int
    price: Price

# @dataclass
# class NewNotification:
#     user_id: int
#     price: Price
