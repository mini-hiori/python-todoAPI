import random
import datetime
import requests
import json
import os

url = os.environ["API_URL"] + "/hello"


def test_hello():
    """
    動作確認用エンドポイント(/hello)が動作することを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    test_task = {
        "task_name": "test_task" + str(random.random()),
        "description": "test_description" + str(random.random()),
    }
    result = requests.get(url, headers=header)
    print(result.text)
    assert result.status_code == 200, "Error"
    return json.loads(result.text)
