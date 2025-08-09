# backend/models.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, NVARCHAR, Integer

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(NVARCHAR(4000), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.sysutcdatetime())