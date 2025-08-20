my_todos=[
    { 'todo_id':1, 'todo_name':"Sports", 'todo_desc':"Play Cricket" },
    { 'todo_id':2, 'todo_name':"Learning", 'todo_desc':"Prepare for test" },
    { 'todo_id':3, 'todo_name':"Meditate", 'todo_desc':"Mediate for 20 minutes" },
    { 'todo_id':4, 'todo_name':"Coding", 'todo_desc':"Code for the world" },
]


def delete_todo(todo_id:int):
    global my_todos
    for index, todo in enumerate(my_todos):
        print(f"\n\nIndex is: {index}")
        if todo['todo_id']==todo_id:
            deleted_todo = my_todos.pop(index)
            return {'message':"Todo deleted successfully", 'deleted_todo': deleted_todo}
    return {'error':"Todo with this id is currently not registered. Gracias"}

if __name__ == "__main__":
    print(delete_todo(2))