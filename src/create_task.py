import boto3
from typing import Dict
from schema import InputTask
import traceback
import hashlib
import random
import uuid
from datetime import datetime


def create_task(user_id: str, task: InputTask) -> str:
    """
    DynamoDBに1つitem追加
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("python-todoapi")
        task_id = str(uuid.uuid4())

        put_task = {
            "user_id": user_id,
            "task_id": task_id,
            "task_name": task.task_name,
            "description": task.description,
            "created_at": datetime.now().strftime("%Y%m%d"),
            "updated_at": datetime.now().strftime("%Y%m%d"),
        }
        table.put_item(Item=put_task)
        return task_id
    except BaseException:
        print(traceback.format_exc())
        return None
