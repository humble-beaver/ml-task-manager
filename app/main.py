"""Entrypoint for the Task Manager API Server"""
import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, status
from sqlmodel import Session, select
from .models.task import Task, TaskRead
from .utils import save_file, process_config
from .data import db
from .controllers.ssh.handler import RemoteHandler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function for initialization and shutting down functions"""
    db.init_db()
    os.makedirs('app/tmp', exist_ok=True)
    yield
    shutil.rmtree('app/tmp')

app = FastAPI(lifespan=lifespan)


def atena_upload(fname):
    """Submit job to atena cluster"""
    host = "slurmmanager"
    user = "admin"
    passwd = "admin"
    remote = RemoteHandler()
    remote.connect(host, user, passwd)
    sanity_check = remote.send_file(fname)
    if not sanity_check:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_200_OK


@app.post("/task/", response_model=TaskRead)
async def create_task(files: list[UploadFile]):
    """Create new task and save it to DB"""
    for file in files:
        fname = file.filename
        fdata = await file.read()
        fpath = save_file(fname, fdata)
        if ".json" in fname:
            task = process_config(fpath)
        if ".py" in fname:
            atena_upload(fname)
    with Session(db.engine) as session:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/task/", response_model=list[Task])
async def get_tasks():
    """Retrieve all saved tasks"""
    with Session(db.engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/task/{task_id}", response_model=TaskRead)
async def get_task_by_id(task_id: int):
    """Retrieve single record of Task that corresponds to given id"""
    with Session(db.engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
