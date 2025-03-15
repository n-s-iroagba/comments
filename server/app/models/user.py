from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base

from app.models.SocialMediaAccount import SocialMediaAccount
from app.models.comment_group import CommentGroup
# from . import CommentGroup
# from .comment import Comment
# from .SocialMediaAccount import SocialMedia
# from .comment_group import CommentGroup

from .base import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    contactID: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    username: Mapped[str]
    contactType: Mapped[str]
    password: Mapped[str]

    # Relationships
    comment_groups: Mapped[List['CommentGroup']] = relationship()
    social_medias: Mapped[List["SocialMediaAccount"]] = relationship()

    def __repr__(self):
        return f"<User {self.username}>"


# class CommentGroup(Base):
#     __tablename__ = "comment_group"

#     id: Mapped[int] = mapped_column(primary_key=True)

#     # Relationships
#     comments: Mapped[List["Comment"]] = relationship(back_populates="comment_group")
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
#     user: Mapped["User"] = relationship(back_populates="commment_groups")


#     def __repr__(self):
#         return f"<CommentGroup {self.id}>"