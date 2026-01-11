from dataclasses import dataclass

@dataclass
class Proxy:
    proxy: str
    user: str
    password: str