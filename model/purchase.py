from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Purchase:
    id: str
    book_id: str
    reader_id: str
    price: float
    purchase_date: datetime = field(default_factory=datetime.now)
