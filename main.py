import os

# import httpx
import pytz
# from dotenv import load_dotenv
from fastapi import FastAPI  # , Body, Request
# from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# from starlette.responses import JSONResponse

from api import ptt
from dotenv import load_dotenv

load_dotenv()
PTT_API_URL = os.getenv("PTT_API_URL")
app = FastAPI(
    title="PTT WebServer",
    description="這是一個查詢與修改PTT文章資料庫的API",
    version="1.0.0"
)
app.include_router(ptt.router)
tz = pytz.timezone("Asia/Taipei")

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", tags=["Index"])
def read_index():
    return FileResponse("static/index.html")
