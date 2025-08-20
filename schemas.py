from pydantic import BaseModel, Field
from typing import Optional
from pydantic.config import ConfigDict
from models import Priority


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=100, description="Name")
    todo_desc: str = Field(..., description="Description")
    priority: Priority = Field(default=Priority.LOW, description="1..3 (HIGH..LOW)")


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=100, description="Name")
    todo_desc: Optional[str] = Field(None, description="Description")
    priority: Optional[Priority] = Field(None, description="1..3 (HIGH..LOW)")


class TodoResponse(TodoBase):
    todo_id: int
    model_config = ConfigDict(from_attributes=True)  
