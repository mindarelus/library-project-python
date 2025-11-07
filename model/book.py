from dataclasses import dataclass, field
from typing import List, Union
from datetime import datetime

@dataclass
class Rating:
    reader_id: str
    value: int             # 1..5
    comment: str = ""

@dataclass
class Book:
    id: Union[str, None]
    title: str
    author_id: str
    description: str
    price: float
    content_path: str  # Path to the .txt file
    publish_date: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    ratings: List[Rating] = field(default_factory=list)

    def get_average_rating(self) -> (float, int):
        """Calculates the average rating and the number of ratings."""
        if not self.ratings:
            return 0.0, 0
        total_value = sum(r.value for r in self.ratings)
        return total_value / len(self.ratings), len(self.ratings)