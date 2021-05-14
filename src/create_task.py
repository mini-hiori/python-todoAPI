import boto3
from typing import Dict
from src.schema import Task

def create_task(task: Task) -> None:
    """
    DynamoDBに1つitem追加
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('テーブル名')
    put_task = {
        "user_id": task.user_id,
        "task_id": task.task_id
        "task_name": task.task_name,
        "description": task.description,
        "created_at": task.created_at
    }
    table.put_item(Item=put_task)
    return None