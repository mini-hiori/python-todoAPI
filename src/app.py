from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schema import Task, InputTask, UpdateTask
from typing import Optional
from search_task import search_task_by_id, search_task_by_name
from mangum import Mangum
from create_task import create_task
from update_task import update_task
from delete_task import delete_task
from typing import List
import traceback
from starlette.requests import Request
from authorization import get_userid_from_idtoken
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # 追記により追加
    allow_methods=["*"],  # 追記により追加
    allow_headers=["*"],  # 追記により追加
)

handler = Mangum(app)


@app.get("/hello")
def hello():
    """
    動作確認用
    """
    return {"message": "hello"}


@app.get("/search_task")
def search_task_api(
    request: Request, task_id: Optional[str] = None, task_name: Optional[str] = None
) -> List[Task]:
    """
    タスク検索用API
    ユーザー情報+task_name or での検索を受け付ける。
    task_nameは部分一致でも良い
    """
    user_id = get_userid_from_idtoken(
        request.scope["aws.event"]["headers"]["Authorization"]
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="認証に失敗しています")
    if not task_id and not task_name:
        raise HTTPException(status_code=400, detail="task_idとtask_nameのどちらかは必須です")
    if task_id:
        search_result: Task = search_task_by_id(user_id, task_id)
        if search_result:
            searched_task: List[Task] = [search_result]
        else:
            searched_task = []
    else:
        searched_task: List[Task] = search_task_by_name(user_id, task_name)
    if searched_task:
        result_list = [
            {
                "task_id": i.task_id,
                "task_name": i.task_name,
                "description": i.description,
                "created_at": i.created_at,
                "updated_at": i.updated_at,
            }
            for i in searched_task
        ]
        return result_list
    else:
        raise HTTPException(status_code=400, detail="検索結果がありません")


@app.put("/create_task")
def create_task_api(request: Request, task: InputTask):
    """
    タスク追加用API
    """
    user_id = get_userid_from_idtoken(
        request.scope["aws.event"]["headers"]["Authorization"]
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="認証に失敗しています")
    if not task.task_name:
        raise HTTPException(status_code=400, detail="task_nameは必須です")
    task_id = create_task(user_id, task)
    if task_id:
        return {"task_id": task_id}
    else:
        raise HTTPException(status_code=400, detail="task登録に失敗しました")


@app.post("/update_task")
def update_task_api(request: Request, task: UpdateTask):
    """
    タスク更新用API
    """
    user_id = get_userid_from_idtoken(
        request.scope["aws.event"]["headers"]["Authorization"]
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="認証に失敗しています")
    if not task.task_name or not task.description:
        raise HTTPException(status_code=400, detail="task_nameかdescriptionのどちらかは必須です")
    result = update_task(user_id, task)
    if result:
        return {"result": "OK"}
    else:
        raise HTTPException(status_code=400, detail="指定したtask_idに該当するタスクがありません")


@app.delete("/delete_task")
def delete_task_api(request: Request, task_id: str):
    """
    タスク削除用API
    """
    user_id = get_userid_from_idtoken(
        request.scope["aws.event"]["headers"]["Authorization"]
    )
    if not user_id:
        raise HTTPException(status_code=400, detail="認証に失敗しています")
    result = delete_task(user_id, task_id)
    if result:
        return {"result": "OK"}
    else:
        raise HTTPException(status_code=400, detail="指定したtask_idに該当するタスクがありません")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
