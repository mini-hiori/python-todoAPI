from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    task_id: str
    task_name: str
    description: str
    created_at: str


class InputTask(BaseModel):
    task_name: str
    description: str
    created_at: str


class SearchTask(BaseModel):
    session_id: str
    task_id: str
    task_name: str


class UserInfo(BaseModel):
    user_name: str
    password: str
