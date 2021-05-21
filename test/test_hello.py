import random
import datetime
import requests
import json
import os

url = os.environ["API_URL"] + "/hello"


def test_hello():
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


if __name__ == "__main__":
    test_hello()
