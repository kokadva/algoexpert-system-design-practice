import os
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# DB Settings
from starlette.templating import Jinja2Templates
from fastapi import Request

STATIC_CONTENT_DIR = os.environ.get('STATIC_CONTENT_DIR', 'static')

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
    return {"message": "static-website-app <3"}


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
