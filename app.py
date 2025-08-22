from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from db import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# origins = [
#     "http://localhost:5173",
#     "http://localhost",
#     "http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Dependency → for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Index
@app.get("/")
def index():
    return {"message": "Hola gracias"}


# CREATE
@app.post("/todos", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(
        todo_name=todo.todo_name,
        todo_desc=todo.todo_desc,
        priority=todo.priority
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# READ - all
@app.get("/todos", response_model=List[schemas.TodoResponse])
def get_todos(first_n: int = 0, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    if first_n != 0 and first_n <= len(todos):
        return todos[:first_n]
    elif first_n > len(todos):
        raise HTTPException(status_code=404, detail=f"We didn't have {first_n} todos to do")
    return todos


# READ - single
@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# UPDATE
@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, updated_todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if updated_todo.todo_name is not None:
        todo.todo_name = updated_todo.todo_name

    if updated_todo.todo_desc is not None:
        todo.todo_desc = updated_todo.todo_desc
    if updated_todo.priority is not None:
        todo.priority = updated_todo.priority

    db.commit()
    db.refresh(todo)
    return todo


# DELETE
@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return todo
