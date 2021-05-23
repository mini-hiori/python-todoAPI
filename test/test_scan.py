import datetime
import requests
import json
import os

url = os.environ["API_URL"] + "/scan_task"


def test_scan():
    """
    scan_taskが成功することを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    result = requests.get(url, headers=header)
    print(result.text)
    assert result.status_code == 200, "Error:test_create"
    return json.loads(result.text)[0]["task_id"]