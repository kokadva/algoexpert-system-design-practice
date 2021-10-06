import datetime
import os
import random
import string
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB Settings
SQLALCHEMY_DATABASE_URL = USER = os.getenv('DB_URI', "postgresql://dev:dev@localhost:5432/dev")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DB Model
class DeploymentJobs(Base):
    __tablename__ = "DEPLOYMENT_JOBS"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default='PENDING')
    commit_code = Column(String, default='')
    last_modified = Column(DateTime, default=datetime.datetime.utcnow)


def create_tables():
    DeploymentJobs.__table__.create(engine)

# Once run creates tables in the DB
# create_tables()

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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Endpoints

@app.get("/ping")
async def ping():
    return {"message": "repo-listener <3"}


@app.post("/repo-webhook")
async def root(request: Request):
    deployment_job = DeploymentJobs(commit_code=id_generator())
    session = SessionLocal()
    session.add(deployment_job)
    session.commit()
    print(await request.json())
    return {
        "id": deployment_job.id.__str__(),
        "status": deployment_job.status,
        "commit_code": deployment_job.commit_code,
        "last_modified": deployment_job.last_modified.__str__()
    }
