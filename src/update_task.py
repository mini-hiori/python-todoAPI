import boto3
from typing import Dict
import traceback
from search_task import search_task_by_id
from schema import UpdateTask
from datetime import datetime


def update_task(user_id: str, task: UpdateTask) -> bool:
    """
    DynamoDB内のタスクを更新
    """
    is_task_exists = search_task_by_id(user_id, task.task_id)
    if is_task_exists:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("python-todoapi")
        table.update_item(
            Key={"user_id": user_id, "task_id": task.task_id},
            UpdateExpression="""
            set
                task_name = :task_name,
                description = :description,
                updated_at = :updated_at
            """,
            ExpressionAttributeValues={
                ":task_name": task.task_name,
                ":description": task.description,
                ":updated_at": datetime.now().strftime("%Y%m%d"),
            },
        )
        return True
    else:
        return False
