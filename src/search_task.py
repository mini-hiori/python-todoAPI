from schema import Task
from datetime import datetime
from boto3.dynamodb.conditions import Key
import boto3
from typing import List


def search_task_by_id(user_id: str, task_id: str) -> Task:
    """
    user_idとtask_idでtaskを検索する
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    search_result = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id) & Key("task_id").eq(task_id)
    )
    if search_result.get("Items"):
        # 検索成功
        result = Task(
            task_name=search_result["Items"][0]["task_name"],
            created_at=search_result["Items"][0]["created_at"],
            updated_at=search_result["Items"][0]["updated_at"],
            description=search_result["Items"][0]["description"],
            task_id=search_result["Items"][0]["task_id"],
        )
        return result
    else:
        return None


def search_task_by_name(user_id: int, task_name: str) -> List[Task]:
    """
    task_nameでtaskを検索する
    ※want to do。多分必須ではないが、普通のユースケースを考えたら存在するべきではある
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    search_result = table.query(
        # 設定したLSIのインデックスNameを指定する
        IndexName="task_name_key",
        KeyConditionExpression=Key("user_id").eq(user_id)
        & Key("task_name").begins_with(task_name),
    )
    if search_result.get("Items"):
        # 検索成功
        result_list = []
        for i in search_result["Items"]:
            task = search_task_by_id(user_id, i["task_id"])
            result_list.append(task)
        return result_list
    else:
        return None
