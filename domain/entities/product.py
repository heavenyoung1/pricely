from dataclasses import dataclass


@dataclass
class Product:
    id: int
    article: str
    name: str
    link: str
    change: int

    @staticmethod
    def create(
        *,
        article: str,
        name: str,
        link: str,
        change: int,
    ) -> 'Product':
        return Product(id=None, article=article, name=name, link=link, change=change)
