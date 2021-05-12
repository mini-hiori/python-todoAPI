from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    task_id: int
    task_name: str
    description: str
    created_date: str
    created_by: str  # 作成者ユーザー名
    created_by_id: int  # 作成者id
