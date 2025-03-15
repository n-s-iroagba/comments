from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from .comment import Comment


class CommentGroup(Base):
    __tablename__ = "comment_group"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    comments: Mapped[List["Comment"]] = relationship()
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))


    def __repr__(self):
        return f"<CommentGroup {self.id}>"