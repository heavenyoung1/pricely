from dataclasses import dataclass


@dataclass
class Product:
    id: int
    article: str
    name: str
    link: str
