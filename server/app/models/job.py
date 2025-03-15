from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .Target import  Target
from .SocialMediaAccount import SocialMediaAccount
# from comment_group import CommentGroup
from .base import Base
from user import CommentGroup



class Job(Base):
    platform: str
    job_type: str
    config: str
    account: SocialMediaAccount
    target: List[Target]