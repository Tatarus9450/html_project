from fastapi import FastAPI, Form, Request, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 1. Define your Pydantic model
class Todo(BaseModel):
    id: int
    task: str
    owner: str

# 2. In-memory storage
todos: List[Todo] = []

# 3. Show homepage with list of todos
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": todos}
    )

# 4. Create new todo (from form)
@app.post("/create-todo")
def create_todo(
    id: int    = Form(...),
    task: str  = Form(...),
    owner: str = Form(...)
):
    # Prevent duplicate IDs
    if any(t.id == id for t in todos):
        raise HTTPException(status_code=400, detail="ID ซ้ำ")
    todo = Todo(id=id, task=task, owner=owner)
    todos.append(todo)
    return RedirectResponse("/", status_code=303)

# 5. Delete a todo (from form)
@app.post("/delete-todo")
def delete_todo(
    id: int    = Form(...),
    owner: str = Form(...)
):
    for idx, t in enumerate(todos):
        if t.id == id:
            if t.owner != owner:
                raise HTTPException(status_code=403, detail="ลบเฉพาะของเจ้าของได้")
            todos.pop(idx)
            return RedirectResponse("/", status_code=303)
    raise HTTPException(status_code=404, detail="ไม่พบ Todo")
