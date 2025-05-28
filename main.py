import os
from datetime import datetime
from typing import Optional

import httpx
import pytz
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import ptt
from schema.ptt_content import PostSchema, UserSchema, BoardSchema

app = FastAPI()
app.include_router(ptt.router)
tz = pytz.timezone("Asia/Taipei")

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# 回傳 index.html 作為入口（例如 for React）
@app.get("/")
def read_index():
    return FileResponse("static/index.html")


@app.post("/posts")
def add_post(
        title: str = Form(...),
        content: str = Form(...),
        author_name: str = Form(...),
        board_name: str = Form(...),
        created_at: Optional[datetime] = Form(None)):

    data = PostSchema(
        title=title,
        content=content,
        author=UserSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        created_at=created_at if created_at else datetime.now(tz),
    )

    return httpx.post("https://jsonplaceholder.typicode.com/posts", json=dict(data))
