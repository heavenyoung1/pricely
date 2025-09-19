from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    id: str
    username: str
    chat_id: str
    products: List[str] = field(default_factory=list)  # 🔥 правильно!