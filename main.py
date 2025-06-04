import os

import httpx
import pytz
from dotenv import load_dotenv
from fastapi import FastAPI, Body, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api import ptt

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
async def get_post(request: Request):
    query_params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            PTT_API_URL + "/api/posts",
            params=query_params
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
async def get_statistics(request: Request):
    query_params = dict(request.query_params)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            PTT_API_URL + "/api/statistics",
            params=query_params
        )
    return response.json()


@app.post("/posts")
async def forward_post(data_json=Body(..., embed=False)):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            PTT_API_URL + "/api/posts",
            json=jsonable_encoder(data_json),
        )
    return response.json()


# --- PUT ---
@app.put("/posts/{post_id}")
async def update_post(post_id: int, data_json=Body(..., embed=False)):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            PTT_API_URL + f"/api/posts/{post_id}",
            json=jsonable_encoder(data_json),
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
