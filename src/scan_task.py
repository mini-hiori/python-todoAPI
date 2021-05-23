from schema import Task
from datetime import datetime
from boto3.dynamodb.conditions import Key
import boto3
from typing import List
from search_task import search_task_by_id


def scan_task(user_id: int) -> List[Task]:
    """
    task全選択用関数
    初手で呼ばれる。一応明示的な検索と区別しておく
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    scan_result = table.scan()
    if scan_result.get("Items"):
        # 検索成功
        result_list = []
        for i in scan_result["Items"]:
            task = search_task_by_id(user_id, i["task_id"])
            if task:
                result_list.append(task)
        return result_list
    else:
        return None
