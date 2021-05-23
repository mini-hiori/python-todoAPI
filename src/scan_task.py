from schema import Task
from datetime import datetime
from boto3.dynamodb.conditions import Key
import boto3
from typing import List


def scan_task(user_id: int) -> List[Task]:
    """
    task_nameでtaskを検索する
    ※want to do。多分必須ではないが、普通のユースケースを考えたら存在するべきではある
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    scan_result = table.scan()
    if scan_result.get("Items"):
        # 検索成功
        result_list = []
        for i in scan_result["Items"]:
            task = search_task_by_id(user_id, i["task_id"])
            result_list.append(task)
        return result_list
    else:
        return None
