from test_create import test_create
import requests
import json
import random
import os

url = os.environ["API_URL"] + "/update_task"


def test_update():
    task_id = test_create()
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    test_task = {
        "task_id": task_id,
        "task_name": "updated_task" + str(random.random()),
        "description": "updated_description" + str(random.random()),
    }
    print(test_task)
    result = requests.post(url, json=test_task, headers=header)
    assert result.status_code == 200, "Error"
    assert json.loads(result.text)["result"] == "OK", "Error"


if __name__ == "__main__":
    task_id = test_create()
    test_update(task_id)
