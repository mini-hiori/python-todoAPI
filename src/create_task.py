import boto3
from typing import Dict
from schema import Task
import traceback
import hashlib
import random
import uuid


def create_task(user_id: str, task: InputTask) -> bool:
    """
    DynamoDBに1つitem追加
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("python-todoapi")

        put_task = {
            "user_id": user_id,
            "task_id": str(uuid.uuid4()),
            "task_name": task.task_name,
            "description": task.description,
            "created_at": task.created_at,
        }
        table.put_item(Item=put_task)
        return True
    except BaseException:
        print(traceback.format_exc())
        return False
