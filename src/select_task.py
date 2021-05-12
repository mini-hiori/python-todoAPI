from src.schema import Task
from datetime import datetime


def select_task_by_id(created_by_id: str, task_id: int) -> Task:
    """
    created_by_idとtask_idでtaskを検索する
    """
    # 仮置き
    task = Task(
        task_id=task_id,
        task_name="test_task",
        description="test",
        created_date=datetime.now().strftime("%Y%m%d"),
        created_by="testuser",
        created_by_id=created_by_id,
    )
    return task


def select_task_by_name(created_by_id: str, task_name: str) -> Task:
    """
    task_nameでtaskを検索する
    """
    # 仮置き
    task = Task(
        task_id=-1,
        task_name=task_name,
        description="test",
        created_date=datetime.now().strftime("%Y%m%d"),
        created_by="testuser",
        created_by_id=created_by_id,
    )
    return task
