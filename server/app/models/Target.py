from typing import List

from .base import Base


class Target(Base):
    url: str
    required_number_of_replies: int
    replies: List[str]