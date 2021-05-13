from src.schema import Task
from datetime import datetime


def search_task_by_id(user_id: str, task_id: int) -> Task:
    """
    user_idとtask_idでtaskを検索する
    """
    # 仮置き
    task = Task(
        user_id=user_id,
        task_id=task_id,
        task_name="test_task",
        description="description",
        created_at="20210514"
    )
    return task


def search_task_by_name(user_id: str, task_name: str) -> Task:
    """
    task_nameでtaskを検索する
    ※want to do。多分必須ではないが、普通のユースケースを考えたら存在するべきではある
    """
    # 仮置き
    task = Task(
        user_id=user_id,
        task_id=-1,
        task_name=task_name,
        description="description",
        created_at="20210514"
    )
    return task
