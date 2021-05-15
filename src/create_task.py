import boto3
from typing import Dict
from schema import Task
import traceback
import hashlib
import random


def create_task(task: Task) -> bool:
    """
    DynamoDBに1つitem追加
    """
    user_id = -1
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("python-todoapi")

        put_task = {
            "user_id": user_id,
            "task_name": task.task_name,
            "description": task.description,
            "created_at": task.created_at,
        }
        table.put_item(Item=put_task)
        return True
    except BaseException:
        print(traceback.format_exc())
        return False


def generate_task_id(user_id: str, task_name: str) -> str:
    """
    taskに対して一意な文字列idを発行する。
    発行するidは必ずtaskテーブルに存在しないものにする
    """
    while True:
        salt = str(random.random())
        task_id = hashlib.sha256(task_name.encode()).hexdigest()
        # DynamoDBをuser_id+task_idで検索して、引っかからなかったらbreak
        result = table.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
            & Key("task_id").begins_with(task_id)
        )
        break
    return task_id
