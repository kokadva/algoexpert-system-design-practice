import os
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from minio import Minio

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


# Minio Config
MINIO_HOST = os.getenv('MINIO_HOST', "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', "access_key")
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', "secret_key")
minio_client = Minio(MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, secure=False)

TMP_DIR = os.environ.get('TMP_DIR', '/Users/kdvalishivli/Desktop/tmp/tmpdata/')
REPO_BASE_URL = os.environ.get('REPO_BASE_URL', 'localhost')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'deployment')


def create_default_bucket(minio_client, bucket_name='deployment'):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)


def get_repo_name(repo_url):
    return 'test-repo'


def clone_commit(repo_url, commit_id, build_id):
    repo_url = repo_url.replace('localhost', REPO_BASE_URL)
    build_dir = TMP_DIR + build_id
    os.makedirs(build_dir)
    os.chdir(build_dir)
    os.system('git clone {repo_url}'.format(repo_url=repo_url))
    repo_name = get_repo_name(repo_url)
    result_path = build_dir + '/' + repo_name + '/'
    os.chdir(result_path)
    os.system('git checkout {commit_id}'.format(commit_id=commit_id))
    return result_path


def upload_build(built_path, bucket_name, build_id, minio_client):
    print("Uploading build from {build_path}".format(build_path=built_path))
    # result = minio_client.fput_object(bucket_name, build_id + '/index.hml', built_path + 'index.html')
    result = minio_client.fput_object(bucket_name, 'build', built_path + 'index.html')
    print("created {0} object; etag: {1}, version-id: {2}".format(result.object_name, result.etag, result.version_id))


PENDING_JOBS_QUERY = "SELECT * FROM \"DEPLOYMENT_JOBS\" WHERE status = 'PENDING' ORDER BY id ASC limit 1"
UPDATE_JOB_TO_PENDING_STATUS_QUERY = \
    'UPDATE "DEPLOYMENT_JOBS" SET status = \'DEPLOYING\', last_modified = now() WHERE id = {job_id}'
UPDATE_JOB_TO_COMPLETE_STATUS_QUERY = \
    'UPDATE "DEPLOYMENT_JOBS" SET status = \'COMPLETE\', last_modified = now() WHERE id = {job_id}'


def query_pending_job():
    session = SessionLocal()
    with session.begin():
        query_result = list(session.execute(text(PENDING_JOBS_QUERY)))
        if len(query_result) == 0: raise Exception("Nothing to work on +_+")
        job_info = query_result[0]
        job_id = job_info[0]
        repo_url = job_info[1]
        commit_id = job_info[2]
        session.execute(text(UPDATE_JOB_TO_PENDING_STATUS_QUERY.format(job_id=str(job_id))))
    return job_id, repo_url, commit_id


def update_finished_job_status(job_id):
    session = SessionLocal()
    with session.begin():
        session.execute(text(UPDATE_JOB_TO_COMPLETE_STATUS_QUERY.format(job_id=str(job_id))))


def handle_repo_event():
    try:
        job_id, repo_url, commit_id = query_pending_job()
    except:
        print("Nothing to do +_+ <3")
        return
    job_id = str(job_id)
    build_path = clone_commit(repo_url, commit_id, job_id)
    upload_build(build_path, BUCKET_NAME, job_id, minio_client)
    update_finished_job_status(job_id)


create_default_bucket(minio_client, BUCKET_NAME)
scheduler = BackgroundScheduler()
scheduler.add_job(handle_repo_event, 'interval', seconds=10)
scheduler.start()
