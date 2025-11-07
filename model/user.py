from dataclasses import dataclass
from typing import Literal

Role = Literal["reader", "author", "admin"]

@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    role: Role
    balance: float = 0.0
    is_banned: bool = False