from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI(
    title="Task Manager API",
    description="",
    docs_url="/",
)
tasks = {}

class CreateTask(BaseModel):
    title: str
    description: str

class Task(CreateTask):
    id: uuid.UUID

@app.post("/tasks", response_model=Task)
def create_task(task: CreateTask):
    task_id = uuid.uuid4()  
    new_task = Task(id=task_id, **task.model_dump()) 
    tasks[str(task_id)] = new_task
    return new_task

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return list(tasks.values())

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    if task_id in tasks:
        return tasks[task_id]
    raise HTTPException(status_code=404, detail="No such task in the list.")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: CreateTask):
    if task_id in tasks:
        updated_task = Task(id=uuid.UUID(task_id), **task_update.model_dump())
        tasks[task_id] = updated_task
        return updated_task
    raise HTTPException(status_code=404, detail="No such task in the list.")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str):
    if task_id in tasks:
        del tasks[task_id]
        return {"message": "Task has been deleted"} 
    raise HTTPException(status_code=404, detail="No such task in the list.")