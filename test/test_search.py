import json
import requests
from test_create import test_create
import os

url = os.environ["API_URL"] + "/search_task"


def test_search_id_succeed():
    """
    task_idベースのsearch_taskが成功することを確認する
    """
    task_id = test_create()
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = os.environ["API_URL"] + f"/search_task?task_id={task_id}"
    alpha = requests.get(url, headers=header)
    print(alpha.text)
    assert json.loads(alpha.text)[0].get("task_id") == task_id, "test_search_id:errored"


def test_search_name_succeed():
    """
    task_nameベースのsearch_taskが成功することを確認する
    """
    task_name = "test_"
    task_id = test_create()
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = os.environ["API_URL"] + f"/search_task?task_name={task_name}"
    alpha = requests.get(url, headers=header)
    print(alpha.text)
    assert (
        json.loads(alpha.text)[0].get("task_name").startswith(task_name)
    ), "test_search_name:errored"


def test_search_multiple_succeed():
    """
    task_idとtask_nameを両方渡してsearch_taskするとidベースの検索になることを確認する
    """
    task_id = test_create()
    task_name = "test_"
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = (
        os.environ["API_URL"] + f"/search_task?task_id={task_id}&task_name={task_name}"
    )
    alpha = requests.get(url, headers=header)
    print(alpha.text)
    assert json.loads(alpha.text)[0].get("task_id") == task_id, "test_search_multiple:errored"
    assert len(json.loads(alpha.text))

def test_search_id_notfound():
    """
    idでの検索結果がない場合は400エラーが帰ることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = (
        os.environ["API_URL"] + f"/search_task?task_id=-1"
    )
    alpha = requests.get(url, headers=header)
    assert alpha.status_code == 400, "test_search_id_notfound:errored"

def test_search_name_notfound():
    """
    nameでの検索結果がない場合は400エラーが帰ることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = (
        os.environ["API_URL"] + f"/search_task?task_name=-1"
    )
    alpha = requests.get(url, headers=header)
    assert alpha.status_code == 400, "test_search_name_notfound:errored"

def test_search_multiple_notfound():
    """
    task_idとtask_nameを両方渡してnotfoundのとき400エラーが帰ることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = (
        os.environ["API_URL"] + f"/search_task?task_id=-1&task_name=-1"
    )
    alpha = requests.get(url, headers=header)
    assert alpha.status_code == 400, "test_search_multiple_notfound:errored"

def test_search_noinput():
    """
    task_idとtask_nameが渡されないとき400エラーが帰ることを確認する
    """
    idtoken = os.environ["IDTOKEN"]
    header = {"Authorization": idtoken}
    url = (
        os.environ["API_URL"] + f"/search_task"
    )
    alpha = requests.get(url, headers=header)
    assert alpha.status_code == 400, "test_search_noinput:errored"