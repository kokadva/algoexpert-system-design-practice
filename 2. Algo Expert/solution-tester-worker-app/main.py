import os
import random
import string

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

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

TMP_DIR = os.getenv('TMP_DIR', 'tmp/')
os.mkdir(TMP_DIR)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Endpoints
@app.get("/solution-tester-worker-app/ping")
async def ping():
    return {"message": "solution-tester-worker-app"}


def test_solution(code):
    tmp_file_name = TMP_DIR + id_generator() + ".py"
    with open(tmp_file_name, "w+") as f:
        f.write(code)
    result = os.popen('python {file_path}'.format(file_path=tmp_file_name)).read()
    return str(result)


@app.post("/solution-tester-worker-app/test")
async def test(request: Request):
    question_solution_info = await request.json()
    result = test_solution(question_solution_info['code'])
    return {
        "result": result
    }
