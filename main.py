from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from api import ptt
app = FastAPI()
app.include_router(ptt.router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# 回傳 index.html 作為入口（例如 for React）
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

