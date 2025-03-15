from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base


from .base import Base


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    comment_group_id: Mapped[int] = mapped_column(ForeignKey('comment_group.id'))

    def __repr__(self):
        return f"<Comment {self.id}: {self.content[:20]}>"
    
