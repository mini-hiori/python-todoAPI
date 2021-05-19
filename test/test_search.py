import json
import requests
from test_create import test_create
import os

url = os.environ["API_URL"] + "/search_task"


def test_search_id_succeed(task_id: str):

    url = os.environ["API_URL"] + f"/search_task?task_id={task_id}"
    alpha = requests.get(url)
    print(alpha.text)
    assert json.loads(alpha.text)[0].get("task_id"), "test_search_id:errored"


def test_search_name_succeed(task_name: str):

    url = os.environ["API_URL"] + f"/search_task?task_name={task_name}"
    alpha = requests.get(url)
    print(alpha.text)
    assert json.loads(alpha.text)[0].get("task_id"), "test_search_id:errored"


if __name__ == "__main__":
    task_id = test_create()
    test_search_id_succeed(task_id)
    test_search_name_succeed("test_")
