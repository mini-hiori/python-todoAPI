import boto3
from typing import Dict

def delete_task(task_id: str) -> None:
    """
    DynamoDBから情報を削除
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('テーブル名')
    table.delete_item(Key={"task_id": task_id})
    return None