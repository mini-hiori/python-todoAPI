from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schema import Task
from typing import Optional
from src.select_task import select_task_by_id, select_task_by_name
from mangum import Mangum

app = FastAPI()


@app.get("/")
def health_check():
    # 動作確認用ルートエンドポイント
    return {"message":"hello"}


@app.get("/select_task", response_model=Task)
def select_task(
    user_id: int, task_id: Optional[int] = None, task_name: Optional[str] = None
):
    """
    タスク検索用API
    ユーザー情報(仮でuser_id)+task_id or task_nameでの検索を受け付ける。
    task_idとtask_nameが同時に渡された場合はtask_idでの検索を優先する
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="ユーザーIDは必須です")
    if not task_id and not task_name:
        raise HTTPException(status_code=400, detail="task_idとtask_nameのどちらかは必須です")
    if task_id:
        selected_task: Task = select_task_by_id(user_id, task_id)
    else:
        selected_task: Task = select_task_by_name(user_id, task_name)
    return JSONResponse(content=jsonable_encoder(selected_task))


handler = Mangum(app)
