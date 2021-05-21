import random
import datetime
import requests
import json
import os

url = os.environ["API_URL"] + "/create_task"


def test_create():
    """
    create_taskが成功することを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    test_task = {
        "task_name": "test_task" + str(random.random()),
        "description": "test_description" + str(random.random()),
    }
    result = requests.put(url, json=test_task, headers=header)
    print(result.text)
    assert result.status_code == 200, "Error"
    return json.loads(result.text)["task_id"]
