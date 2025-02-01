from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import local_session, engine
from models import Task, CreateTask, base
import uuid

app = FastAPI(
    title="Task Manager API",
    description="",
    docs_url="/",
)

base.metadata.create_all(bind=engine)

def get_database():
    db = local_session()
    try: yield db
    finally: db.close()

def no_task_exception():
    raise HTTPException(status_code=404, detail="No such task in the list.")

@app.post("/tasks", response_model=CreateTask)
def create_task(task_data: CreateTask, db: Session = Depends(get_database)):
    task_id = uuid.uuid4()  
    new_task = Task(id=str(task_id), title=task_data.title, description=task_data.description) 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks", response_model=list[CreateTask])
def get_tasks(db: Session = Depends(get_database)):
    return db.query(Task).all()

@app.get("/tasks/{task_id}", response_model=CreateTask)
def get_task(task_id: str, db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        no_task_exception()
    return task

@app.put("/tasks/{task_id}", response_model=CreateTask)
def update_task(task_id: str, task_data: CreateTask, db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        no_task_exception()
    task.title = task_data.title
    task.description = task_data.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_database)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        no_task_exception()
    db.delete(task)
    db.commit()
    return {"message": "Task has been deleted"} 
