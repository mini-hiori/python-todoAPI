from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schema import Task, InputTask, SearchTask
from typing import Optional
from search_task import search_task_by_id, search_task_by_name
from mangum import Mangum
from create_task import create_task

app = FastAPI()


@app.get("/search_task", response_model=Task)
def search_task(query: SearchTask):
    """
    タスク検索用API
    ユーザー情報+task_name or での検索を受け付ける。
    task_nameは部分一致でも良い
    """
    if not query.task_id and not query.task_name:
        raise HTTPException(status_code=400, detail="task_idとtask_nameのどちらかは必須です")
    if query.task_id:
        searched_task: Task = search_task(user_id, query.task_name)
    else:
        searched_task: Task = search_task_by_name(user_id, query.task_name)
    return JSONResponse(content=jsonable_encoder(searched_task))


@app.put("/create_task")
def create_task(task: InputTask):
    """
    タスク追加用API
    """
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    result = create_task(task)
    if result:
        return True
    else:
        raise HTTPException(status_code=502, detail="登録時エラーが発生しました")


@app.post("/update_task")
def update_task(task: InputTask):
    """
    タスク追加用API
    """
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    result = create_task(task)
    if result:
        return True
    else:
        raise HTTPException(status_code=502, detail="登録時エラーが発生しました")


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
        raise HTTPException(status_code=502, detail="登録時エラーが発生しました")


handler = Mangum(app)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
