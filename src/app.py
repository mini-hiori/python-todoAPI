from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schema import Task, InputTask, SearchTask
from typing import Optional
from search_task import search_task_by_id, search_task_by_name
from mangum import Mangum
from create_task import create_task
from update_task import update_task
from typing import List
import traceback

app = FastAPI()


@app.get("/hello")
def hello():
    """
    動作確認用
    """
    return {"message": "hello"}


@app.get("/search_task")
def search_task(task_id: Optional[str] = None, task_name: Optional[str] = None) -> List[Task]:
    """
    タスク検索用API
    ユーザー情報+task_name or での検索を受け付ける。
    task_nameは部分一致でも良い
    """
    user_id = "-1"  # TODO:あとで、認証してuser_idを引く処理を入れる
    if not task_id and not task_name:
        raise HTTPException(status_code=400, detail="task_idとtask_nameのどちらかは必須です")
    try:
        if task_id:
            searched_task: List[Task] = [search_task_by_id(user_id, task_id)]
        else:
            searched_task: List[Task] = search_task_by_name(user_id, task_name)
    except:
        print(traceback.format_exc())
    if searched_task:
        result_list = [
            {
                "task_id": i.task_id,
                "task_name": i.task_name,
                "description": i.description,
                "created_at": i.created_at,
            }
            for i in searched_task
        ]
        return result_list
    else:
        raise HTTPException(status_code=400, detail="検索結果がありません")


@app.put("/create_task")
def create_task(task: InputTask):
    """
    タスク追加用API
    """
    user_id = "-1"  # TODO:あとで、認証してuser_idを引く処理を入れる
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    result = create_task(user_id, task)
    if result:
        return "OK"
    else:
        raise HTTPException(status_code=500, detail="登録時エラーが発生しました")


@app.post("/update_task")
def update_task(task: InputTask):
    """
    タスク更新用API
    """
    user_id = "-1"  # TODO:あとで、認証してuser_idを引く処理を入れる
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    result = update_task(user_id, task)
    if result:
        return True
    else:
        raise HTTPException(status_code=500, detail="登録時エラーが発生しました")


@app.delete("/delete_task")
def delete_task(task: InputTask):
    """
    タスク追加用API
    """
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    result = create_task(task)
    if result:
        return True
    else:
        raise HTTPException(status_code=500, detail="削除時エラーが発生しました")


handler = Mangum(app)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
