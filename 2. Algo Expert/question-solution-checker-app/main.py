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


# Endpoints
@app.get("/question-solution-checker-app/ping")
async def ping():
    return {"message": "question-solution-checker-app"}


def test_solution(code):
    print("Testing solution:", code)
    # TODO implement
    return "SUCCESS/FAIL"


@app.post("/question-solution-checker-app/solutions")
async def test_solution(request: Request):
    question_solution_info = await request.json()
    result = test_solution(question_solution_info['code'])
    return {
        "result": result
    }
