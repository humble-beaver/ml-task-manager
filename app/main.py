"""Entrypoint for the Task Manager API Server"""
import os
import shutil
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, status
from sqlmodel import Session, SQLModel, create_engine, select
from .models.task import Task, TaskRead
from .utils import save_file, process_config, get_status_message
from .controllers.ssh.handler import RemoteHandler
from .controllers.slurm.slurm_manager import prep_template


SQLITE_FILE_NAME = "database.db"
sqlite_url = f"sqlite:///{SQLITE_FILE_NAME}"
engine = create_engine(sqlite_url, echo=True)


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
    # TODO: FIX: this is not running when using `scancel`
    shutil.rmtree('app/tmp')

app = FastAPI(lifespan=lifespan)


def atena_connect():
    """Spawn new remote handler with atena config

    :return: remote handler object connected to atena
    :rtype: RemoteHandler
    """
    remote = RemoteHandler()
    # TODO: adjust to the API's user
    host = "atn1mg4"
    user = os.environ["USER"]
    passwd = os.environ["KEY_ATENA"]
    remote.connect(host, user, passwd)
    return remote


def dev_connect():
    """Spawn new remote handler with dev config

    :return: remote handler object connected to dev slurm
    :rtype: RemoteHandler
    """
    remote = RemoteHandler()
    host = "slurmmanager"
    user = "admin"
    passwd = "admin"
    remote.connect(host, user, passwd)
    return remote


def atena_upload(fname, remote):
    """Submit job to atena cluster"""
    sanity_check = remote.send_file(fname)
    if not sanity_check:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_200_OK


def dev_upload(fname, remote):
    """Submit job to local dev cluster"""
    sanity_check = remote.send_file(fname)
    if not sanity_check:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    return status.HTTP_200_OK


# Atena 02 only but with a more generic name
@app.post("/new_task/", response_model=TaskRead)
async def create_task(files: list[UploadFile]):
    """Create new task and save it to DB"""
    remote = atena_connect()
    for file in files:
        fname = file.filename
        fdata = await file.read()
        fpath = save_file(fname, fdata)
        if ".json" in fname:
            task = process_config(fpath)
        if ".py" in fname:
            atena_upload(fname, remote)
    srm_path = prep_template(task)
    atena_upload(srm_path, remote)
    remote.exec(f"sbatch {os.environ['FOLDER']}/{srm_path}")
    job_id = remote.get_output()[0].split('Submitted batch job ')[1][:-1]
    remote.close()
    task['job_id'] = job_id
    with Session(engine) as session:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


@app.get("/tasks/", response_model=list[Task])
async def get_tasks():
    """Retrieve all saved tasks"""
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks


@app.get("/job_status/{job_id}")
async def get_job_status(job_id: int):
    """Retrieve job status given ID"""
    remote = atena_connect()
    # TODO: Adjust squeue params to prevent using try-except for ended job
    # check squeue --help for options
    remote.exec(f"squeue -j {job_id}")
    output = remote.get_output()[0]
    job_status = output.splitlines()[1].split()[4]
    return get_status_message(job_status)

# @app.get("/task/{task_id}", response_model=TaskRead)
# async def get_task_by_id(task_id: int):
#     """Retrieve single record of Task that corresponds to given id"""
#     with Session(engine) as session:
#         task = session.get(Task, task_id)
#         if not task:
#             raise HTTPException(status_code=404, detail="Task not found")
#         return task


if __name__ == "__main__":
    create_db_and_tables()
