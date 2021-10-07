import os
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# DB Settings
SQLALCHEMY_DATABASE_URL = USER = os.getenv('DB_URI', "postgresql://dev:dev@localhost:5432/dev")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI Init
app = FastAPI()

# Cors settings
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints
@app.get("/ping")
async def ping():
    return {"message": "repo-listener <3"}


TMP_DIR = os.environ.get('TMP_DIR', '/Users/kdvalishivli/Desktop/tmp/tmpdata/')
REPO_BASE_URL = os.environ.get('REPO_BASE_URL', 'localhost')

def get_repo_name(repo_url):
    return 'test-repo'


def clone_commit(repo_url, commit_id):
    print("Cloning")
    repo_url = repo_url.replace('localhost', REPO_BASE_URL)
    print("Repo URL", repo_url)
    build_dir = TMP_DIR + uuid.uuid4().hex.upper()[0:6]
    os.makedirs(build_dir)
    print("Build Dir", build_dir)
    os.chdir(build_dir)
    os.system('git clone {repo_url}'.format(repo_url=repo_url))
    repo_name = get_repo_name(repo_url)
    result_path = build_dir + '/' + repo_name
    os.chdir(result_path)
    os.system('git checkout {commit_id}'.format(commit_id=commit_id))
    return result_path


def upload_build(built_path):
    print("Uploading build from {build_path}".format(build_path=built_path))
    # TODO implement


PENDING_JOBS_QUERY = "SELECT * FROM \"DEPLOYMENT_JOBS\" WHERE status = 'PENDING' ORDER BY id ASC limit 1"
UPDATE_JOB_STATUS_QUERY = 'UPDATE "DEPLOYMENT_JOBS" SET status = \'DEPLOYING\' WHERE id = {job_id}'


def query_pending_job():
    session = SessionLocal()
    with session.begin():
        query_result = list(session.execute(text(PENDING_JOBS_QUERY)))
        if len(query_result) == 0: raise Exception("Nothing to work on +_+")
        job_info = query_result[0]
        repo_url = job_info[1]
        commit_id = job_info[2]
        session.execute(text(UPDATE_JOB_STATUS_QUERY.format(job_id=str(job_info[0]))))
    return repo_url, commit_id


def handle_repo_event():
    try:
        repo_url, commit_id = query_pending_job()
    except:
        print("Nothing to do +_+ <3")
        return
    build_path = clone_commit(repo_url, commit_id)
    upload_build(build_path)


scheduler = BackgroundScheduler()
scheduler.add_job(handle_repo_event, 'interval', seconds=10)
scheduler.start()