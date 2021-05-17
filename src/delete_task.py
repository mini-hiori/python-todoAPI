import boto3
from typing import Dict
import traceback


def delete_task(user_id: str, task_id: str) -> bool:
    """
    DynamoDBからタスクを削除
    """
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("python-todoapi")
        table.delete_item(Key={"user_id": user_id, "task_id": task_id})
        return True
    except BaseException:
        print(traceback.format_exc())
        return False
