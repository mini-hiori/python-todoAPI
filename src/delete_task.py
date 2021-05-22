import boto3
from typing import Dict
import traceback
from search_task import search_task_by_id


def delete_task(user_id: str, task_id: str) -> bool:
    """
    DynamoDBからタスクを削除
    """
    is_task_exists = search_task_by_id(user_id, task_id)
    if not is_task_exists:
        return False
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    table.delete_item(Key={"user_id": user_id, "task_id": task_id})
    return True
