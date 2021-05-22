from test_create import test_create
import requests
import json
import os

url = os.environ["API_URL"] + "/delete_task"


def test_delete():
    """
    delete_taskが成功することを確認する
    """
    task_id = test_create()
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    target_url = url + f"?task_id={task_id}"
    result = requests.delete(target_url, headers=header)
    print(result.text)
    assert result.status_code == 200, "Error:test_delete"
    assert json.loads(result.text)["result"] == "OK", "Error:test_delete"
    search_url = os.environ["API_URL"] + f"/search_task?task_id={task_id}"
    search_result = requests.get(search_url, headers=header)
    assert search_result.status_code == 400, "Error:test_delete"  # きちんと消えていることを確認


def test_delete_invalidid():
    """
    delete_taskに存在しないtask_idを渡すと400エラーとなることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    target_url = url + f"?task_id=invalidid"
    result = requests.delete(target_url, headers=header)
    print(result.text)
    assert result.status_code == 400, "Error:test_delete"
