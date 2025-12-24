from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING


@dataclass
class Product:
    id: str
    user_id: str
    name: str
    link: str
    created_at: datetime

