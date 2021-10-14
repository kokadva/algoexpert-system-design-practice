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
SQLALCHEMY_DATABASE_URL = os.getenv('DB_URI', "postgresql://dev:dev@localhost:5432/dev")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# DB Model
class Questions(Base):
    __tablename__ = "QUESTIONS"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)


def create_tables():
    try:
        Questions.__table__.create(engine)
        print("Created tables")
    except:
        pass


# Once run creates tables in the DB
create_tables()


def create_questions():

    session = SessionLocal()
    session.execute('DELETE FROM "QUESTIONS"')
    for k in range(10):
        question = Questions(text=str(k) + ' question ?')
        session.add(question)
    session.commit()


create_questions()

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
@app.get("/questions-server-app/ping")
async def ping():
    return {"message": "questions-server-app <3"}


@app.get("/questions-server-app/questions")
async def get_questions():
    session = SessionLocal()
    records = session.query(Questions).all()
    result = {}
    for r in records:
        result[r.id] = {
            'id': r.id,
            'text': r.text
        }
    return result
