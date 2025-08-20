from fastapi import FastAPI, HTTPException

from typing import List, Optional
from enum import IntEnum
from pydantic import BaseModel, Field

api = FastAPI()

class Priority(IntEnum):
    LOW=3
    MEDIUM=2
    HIGH=1

class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=100, description="Name of the todo item")
    todo_desc: str = Field(..., description="Description of the todo item")
    priority: Priority=Field(default=Priority.LOW, description="Priority of the todo item, You can change between 1 to 3")

class TodoCreate(TodoBase):
    pass 

class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique identifier for the todo item")


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=100, description="Name of the todo item")
    todo_desc: Optional[str] = Field(None, description="Description of the todo item")
    priority: Optional[Priority]=Field(None, description="Priority of the todo item, You can change between 1 to 3")


my_todos=[
    Todo(todo_id=1, todo_name="Sports", todo_desc="Play Cricket", priority=Priority.MEDIUM),
    Todo(todo_id=2, todo_name="Learning", todo_desc="Prepare for test", priority=Priority.HIGH),
    Todo(todo_id=3, todo_name="Meditate", todo_desc="Mediate for 20 minutes", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Coding", todo_desc="Code for the world", priority=Priority.MEDIUM),
]

# In General Api: 
@api.get('/')
def index():
    return {'message':'hola gracias'}


# Create Api:
@api.post('/todos', response_model=Todo)
def create_todo(todo:TodoCreate):
    new_todo_id=max(todo.todo_id for todo in my_todos) + 1
    new_todo=Todo(
        todo_id=new_todo_id,
        todo_name=todo.todo_name,
        todo_desc=todo.todo_desc,
        priority=todo.priority
    )
    my_todos.append(new_todo)
    return new_todo


# Read Api: 
@api.get('/todos', response_model=List[Todo])
def  get_todos(first_n:int):
    if first_n != 0 and first_n <= len(my_todos):
        return my_todos[:first_n]
    elif (first_n > len(my_todos)):
        return {'message':f"We didn't have {first_n} todos to do"}


# Read Api with id:
@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id:int):
    for todo in my_todos:
        if todo.todo_id == todo_id:
            return todo
    return{'error':"todo with this id is currently not registered. Gracias"}


# Update Api: 
@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id:int, updated_todo:TodoUpdate):
    for todo in my_todos:
        if todo.todo_id == todo_id:
            todo.todo_name = updated_todo.todo_name if updated_todo.todo_name is not None else todo.todo_name

            todo.todo_desc = updated_todo.todo_desc if updated_todo.todo_desc is not None else todo.todo_desc

            todo.priority = updated_todo.priority if updated_todo.priority is not None else todo.priority

            return todo
    raise HTTPException(status_code=404, detail="Todo with this id is not found.")


# Delete Api:
@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id:int):
    for todo in my_todos:
        if todo.todo_id == todo_id:
            my_todos.remove(todo)
            return todo
    raise HTTPException(status_code=404, detail="Todo with this id is not found.")


