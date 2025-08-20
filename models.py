from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from db import Base
import enum


class Priority(enum.IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Todo(Base):
    __tablename__ = "todos"

    todo_id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    todo_name:Mapped[str] = mapped_column(String, index=True)
    todo_desc:Mapped[str] = mapped_column(String)
    priority:Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.LOW)




