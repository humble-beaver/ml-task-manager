from fastapi import FastAPI, UploadFile
from .model.task import Task

app = FastAPI()
fake_db = {0: "initial task"}


@app.get("/")
async def root():
    return {"Message": "Hello World"}


@app.post("/task/create")
async def create_task(task: Task):
    task_dict = task.dict()
    task_id = len(fake_db) + 1
    fake_db[task_id] = {
        "id": task_id,
        **task_dict}
    return task_dict


@app.get("/task/status/{task_id}")
async def get_status(task_id: int):
    return fake_db[task_id]
