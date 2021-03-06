from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import requests
import os

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

QUESTION_TESTER_WORKER_BASE_URL = os.getenv("QUESTION_TESTER_WORKER_BASE_URL",
                                       'http://localhost:5003/solution-tester-worker-app')


# Endpoints
@app.get("/question-solution-checker-app/ping")
async def ping():
    return {"message": "question-solution-checker-app"}


def test_solution(code):
    url = QUESTION_TESTER_WORKER_BASE_URL + '/test'
    data = {'code': code}
    response = requests.post(url, json=data)
    return response.json()['result']


@app.post("/question-solution-checker-app/solutions")
async def test(request: Request):
    question_solution_info = await request.json()
    print()
    result = test_solution(question_solution_info['code'])
    return {
        "result": result
    }
