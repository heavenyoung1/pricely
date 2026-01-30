from dataclasses import dataclass
from typing import List

@dataclass
class UserProducts:
    user_id: int
    product_id: int

@dataclass
class UserProductsData:
    chat_id: int
    product_links: List[str]

@dataclass
class TransferData:
    data: List[UserProductsData]