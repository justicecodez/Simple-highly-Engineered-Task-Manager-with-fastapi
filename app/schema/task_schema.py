from pydantic import BaseModel, Field
from datetime import date 
from app.enum.status import Status
from app.enum.priority import Priority

class TaskSchemaRequest(BaseModel):
    title: str=Field(..., max_length=255)
    description: str=Field(..., max_length=255)
    status: Status
    priority: Priority
    due_date: date

class TaskSchemaUpdate(BaseModel):
    title: str|None
    description: str|None
    status: Status
    priority: Priority
    due_date: date


class TaskSchemaResponse(BaseModel):
    id: int
    title: str
    description: str
    status: Status
    priority: Priority
    due_date: date
    completed_at:date