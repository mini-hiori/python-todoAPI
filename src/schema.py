from pydantic import BaseModel
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    task_id: str
    task_name: str
    description: str
    created_at: str
    updated_at: str


class InputTask(BaseModel):
    task_name: str
    description: str


class UpdateTask(BaseModel):
    task_id: str
    task_name: str
    description: str


class UserInfo(BaseModel):
    user_name: str
    password: str
