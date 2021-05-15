from schema import Task
from datetime import datetime
from boto3.dynamodb.conditions import Key
import boto3


def search_task_by_id(user_id: str, task_id: str) -> List[Task]:
    """
    user_idとtask_idでtaskを検索する
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("python-todoapi")
    response = table.query(
        KeyConditionExpression=Key("user_id").eq(user_id)
        & Key("task_id").begins_with(task_id)
    )
    if search_result.get("Item"):
        # 検索成功
        task = Task(
            task_name=search_result["Item"]["task_name"],
            created_at=search_result["Item"]["created_at"],
            description=search_result["Item"]["description"],
            task_id=search_result["Item"]["task_id"],
        )
        return [task]
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
    print(search_result)
    if search_result.get("Items"):
        # 検索成功
        result_list = [
            Task(
                task_name=i["task_name"],
                created_at=i["created_at"],
                description=i["description"],
                task_id=i["task_id"],
            )
            for i in search_result["Items"]
        ]
        return result_list
    else:
        return None
