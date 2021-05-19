from test_create import test_create
import requests
import json
import os

url = os.environ["API_URL"] + "/delete_task"


def test_delete(task_id: str):
    target_url = url + f"?task_id={task_id}"
    print(target_url)
    result = requests.delete(target_url)
    print(result.text)
    assert result.status_code == 200, "Error"
    assert json.loads(result.text)["result"] == "OK", "Error"


if __name__ == "__main__":
    task_id = test_create()
    test_delete("a")
