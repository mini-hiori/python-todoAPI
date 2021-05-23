from test_create import test_create
import requests
import json
import random
import os

url = os.environ["API_URL"] + "/update_task"


def test_update():
    """
    update_taskが成功することを確認する
    """
    task_id = test_create()
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    update_name = "updated_task" + str(random.random())
    updated_description = "updated_description" + str(random.random())
    test_task = {
        "task_id": task_id,
        "task_name": update_name,
        "description": updated_description,
    }
    print(test_task)
    result = requests.post(url, json=test_task, headers=header)
    assert result.status_code == 200, "Error:test_update"
    assert json.loads(result.text)["result"] == "OK", "Error:test_update"
    search_url = os.environ["API_URL"] + f"/search_task?task_id={task_id}"
    search_result = requests.get(search_url, headers=header)
    assert search_result.status_code == 200, "Error:test_update"
    task_info = json.loads(search_result.text)[0]
    assert (
        task_info["task_name"] == update_name
        and task_info["description"] == updated_description
    ), "Error:test_update"


def test_update_invalidid():
    """
    update_taskに存在しないtask_idを渡すと400エラーとなることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    update_name = "updated_task" + str(random.random())
    updated_description = "updated_description" + str(random.random())
    test_task = {
        "task_id": "invalidtaskid",
        "task_name": update_name,
        "description": updated_description,
    }
    result = requests.post(url, headers=header, json=test_task)
    print(result.text)
    assert result.status_code == 400, "Error:test_update"


if __name__ == "__main__":
    task_id = test_create()
    test_update(task_id)
