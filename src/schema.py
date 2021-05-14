from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    user_id: int
    task_id: int
    task_name: str
    description: str
    created_at: str
