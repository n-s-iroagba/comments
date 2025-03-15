from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, Float, ForeignKey
from .base import Base
from user import User


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[DateTime] = mapped_column(nullable=False)
    amount: Mapped[Float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.amount}>"
