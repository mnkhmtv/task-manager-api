from database import base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
import uuid 
class Task(base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index = True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)
    description = Column(String)
    
class CreateTask(BaseModel): 
    title: str
    description: str
    
class TaskResponse(BaseModel):
    id: str
    title: str
    description: str