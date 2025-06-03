import os
from datetime import datetime
from typing import Optional

import httpx
import pytz
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Query, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import ptt
from schema.ptt_content import PostSchema, UserSchema, BoardSchema

app = FastAPI()
app.include_router(ptt.router)
tz = pytz.timezone("Asia/Taipei")

static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def read_index():
    return FileResponse("static/index.html")


# 模擬 呼叫第三方API
load_dotenv()
PTT_API_URL = os.getenv("PTT_API_URL")


# --- GET ---
@app.get("/posts")
async def get_post(
        author_name: Optional[str] = Query(""),
        board_name: Optional[str] = Query(""),
        start_datetime: Optional[str] = Query(""),
        end_datetime: Optional[str] = Query(""),
        limit=50,
        page=1
):
    query_string = '&'.join([
        f"author_name={author_name}",
        f"board_name={board_name}",
        f"start_datetime={start_datetime}",
        f"end_datetime={end_datetime}",
        f"limit={limit}",
        f"page={page}"
    ])

    async with httpx.AsyncClient() as client:
        response = await client.get(
            PTT_API_URL + "/api/posts?" + query_string
        )
    return response.json()


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            PTT_API_URL + f"/api/posts/{post_id}"
        )
    return response.json()


@app.get("/statistics")
async def get_statistics(
        author_name: Optional[str] = Query(""),
        board_name: Optional[str] = Query(""),
        start_datetime: Optional[str] = Query(""),
        end_datetime: Optional[str] = Query("")
):
    query_string = '&'.join([
        f"author_name={author_name}",
        f"board_name={board_name}",
        f"start_datetime={start_datetime}",
        f"end_datetime={end_datetime}"
    ])

    async with httpx.AsyncClient() as client:
        response = await client.get(
            PTT_API_URL + "/api/statistics?" + query_string
        )
    return response.json()


# --- POST ---
# @app.post("/posts")
# async def forward_post(
#         title: str = Form(...),
#         content: str = Form(...),
#         author_name: str = Form(...),
#         board_name: str = Form(...)
# ):
#     post_schema = PostSchema(
#         title=title if title else None,
#         content=content if title else None,
#         author=UserSchema(name=author_name) if author_name else None,
#         board=BoardSchema(name=board_name) if board_name else None
#     )
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             PTT_API_URL + "/api/posts",
#             json=jsonable_encoder(post_schema),
#         )
#     return response.json()


@app.post("/posts")
async def forward_post(data=Body(...)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PTT_API_URL + "/api/posts",
            json=jsonable_encoder(data),
        )
    return response.json()


# --- PUT ---
@app.put("/posts/{post_id}")
async def update_post(
        post_id: int,
        title: str = Form(...),
        content: str = Form(...),
        author_name: str = Form(...),
        board_name: str = Form(...),
        created_at: Optional[str] = Form(None)
):
    post_schema = PostSchema(
        title=title if title else None,
        content=content if title else None,
        author=UserSchema(name=author_name) if author_name else None,
        board=BoardSchema(name=board_name) if board_name else None,
        created_at=created_at if created_at else datetime.now(tz)
    )
    async with httpx.AsyncClient() as client:
        response = await client.put(
            PTT_API_URL + f"/api/posts/{post_id}",
            json=jsonable_encoder(post_schema),
        )
    return response.json()


# --- DELETE ---
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            PTT_API_URL + f"/api/posts/{post_id}"
        )
    return response.json()
