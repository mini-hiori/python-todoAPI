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
    assert result.status_code == 200, "Error"
    assert json.loads(result.text)["result"] == "OK", "Error"
