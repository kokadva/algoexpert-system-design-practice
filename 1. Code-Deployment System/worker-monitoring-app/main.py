import os
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


UPDATE_JOB_STATUS_QUERY = 'UPDATE "DEPLOYMENT_JOBS" SET status = \'PENDING\' WHERE status = \'DEPLOYING\' AND EXTRACT(EPOCH FROM (now() - last_modified)) >= 60 * 3'


def update_job_status():
    session = SessionLocal()
    with session.begin():
        session.execute(text(UPDATE_JOB_STATUS_QUERY))


scheduler = BackgroundScheduler()
scheduler.add_job(update_job_status, 'interval', seconds=15)
scheduler.start()
