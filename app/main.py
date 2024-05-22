"""Entrypoint for the Task Manager API Server"""
import hashlib
from fastapi import FastAPI, HTTPException, UploadFile
from sqlmodel import Session, select
from .models.task import Task, TaskRead, TaskCreate

from .data import db


app = FastAPI()


@app.on_event("startup")
def on_startup():
    """Function to run before accepting requests"""
    db.init_db()


@app.post("/atena_submit")
async def atena_submit(files: list[UploadFile]):
    """Submit job to atena cluster"""
    contents = {}
    for file in files:
        contents[file.filename] = await file.read()
        for fname, fcont in contents.items():
            print(fcont)
            with open(f"app/tmp/{fname}", 'wb') as f:
                f.write(fcont)
            with open(f"app/tmp/{fname}.md5", "wb") as f:
                hashmd5 = hashlib.md5(fcont).hexdigest()
                f.write(hashmd5.encode())


@app.post("/task/", response_model=TaskRead)
async def create_task(task: TaskCreate):
    """Create new task and save it to DB

    :param task: JSON Request body with all Task model parameters
    :type task: TaskCreate
    :return: Same data but with assigned id
    :rtype: TaskRead
    """
    with Session(db.engine) as session:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/task/", response_model=list[Task])
async def get_tasks():
    """Retrieve all saved tasks

    :return: List of all tasks
    :rtype: list[Task]
    """
    with Session(db.engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/task/{task_id}", response_model=TaskRead)
async def get_task_by_id(task_id: int):
    """Retrieve single record of Task that corresponds to given id

    :param task_id: the id of the requested task
    :type task_id: int
    :raises HTTPException: A 404 status exception if task not found
    :return: task info
    :rtype: Task
    """
    with Session(db.engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task


@app.get("/test_ssh")
async def test_ssh():
    """Test SSH connection to cluster manager"""
    remote.connect()
    remote.exec("sinfo")
    return remote.get_output()
