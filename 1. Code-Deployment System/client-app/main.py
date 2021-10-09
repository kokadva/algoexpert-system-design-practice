import os
from fastapi.responses import HTMLResponse
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio

# DB Settings
from starlette.templating import Jinja2Templates
from fastapi import Request

MINIO_HOST = os.getenv('MINIO_HOST', "127.0.0.1:9000")
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', "access_key")
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', "secret_key")

minio_client = Minio(MINIO_HOST, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, secure=False)

STATIC_CONTENT_DIR = os.environ.get('STATIC_CONTENT_DIR', 'static')
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'deployment')

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

templates = Jinja2Templates(directory=STATIC_CONTENT_DIR)


# Endpoints
@app.get("/ping")
async def ping():
    return {"message": "repo-listener <3"}


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def create_default_bucket(minio_client, bucket_name='deployment'):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)


def update_build():
    minio_client.fget_object(BUCKET_NAME, "build", "static/index.html")


create_default_bucket(minio_client, BUCKET_NAME)
scheduler = BackgroundScheduler()
scheduler.add_job(update_build, 'interval', seconds=10)
scheduler.start()

objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
