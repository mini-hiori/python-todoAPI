import random
import datetime
import requests
import json
import os

url = os.environ["API_URL"]


def test_unauthorized():
    """
    headerを投げずにリクエストするとunauthorizedになることを確認する
    """
    result_hello = requests.get(url + "/hello")
    result_create = requests.get(url + "/create_task")
    result_search = requests.get(url + "/search_task")
    result_update = requests.get(url + "/update_task")
    result_delete = requests.get(url + "/delete_task")
    result_list = [
        result_hello.status_code,
        result_create.status_code,
        result_search.status_code,
        result_update.status_code,
        result_delete.status_code,
    ]
    assert len(set(result_list)) == 1 and result_list[0] == 401, "Error_Unauthorized"
    return result_list


if __name__ == "__main__":
    test_create()
