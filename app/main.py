"""Entrypoint for the Task Manager API Server"""
import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, status
from sqlmodel import Session, SQLModel, create_engine, select
from .models.task import Task, TaskRead
from .utils import save_file, process_config
from .controllers.ssh.handler import RemoteHandler
from .controllers.slurm.slurm_manager import prep_template


SQLITE_FILE_NAME = "database.db"
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(sqlite_url, echo=True)
remote = RemoteHandler()


def create_db_and_tables():
    """initialize db and tables"""
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function for initialization and shutting down functions"""
    # db.init_db()
    create_db_and_tables()
    os.makedirs('app/tmp', exist_ok=True)
    yield
    shutil.rmtree('app/tmp')

app = FastAPI(lifespan=lifespan)


def atena_upload(fname):
    """Submit job to atena cluster"""
    host = "atn1mg4"
    user = "f5we"
    passwd = "595677#Asd1"
    remote.connect(host, user, passwd)
    sanity_check = remote.send_file(fname)
    if not sanity_check:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_200_OK


def dev_upload(fname):
    """Submit job to local dev cluster"""
    host = "slurmmanager"
    user = "admin"
    passwd = "admin"
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
    srm_path = prep_template(task)
    atena_upload(srm_path)
    remote.exec(f"sbatch /tmp/{srm_path}")
    with Session(engine) as session:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/task/", response_model=list[Task])
async def get_tasks():
    """Retrieve all saved tasks"""
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/task/{task_id}", response_model=TaskRead)
async def get_task_by_id(task_id: int):
    """Retrieve single record of Task that corresponds to given id"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task


if __name__ == "__main__":
    create_db_and_tables()
