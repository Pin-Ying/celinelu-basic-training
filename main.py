from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tasks.celery_tasks import crawl_all_boards
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# 掛載靜態資源資料夾
# 動態取得正確路徑（比較穩定）
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# 回傳 index.html 作為入口（例如 for React）
@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")


@app.post("/crawl")
def trigger_crawl():
    crawl_all_boards.delay()
    return {"message": "Crawling task has been triggered"}


@app.get("/crawl/{board}")
def trigger_crawl_board(board: str):
    crawl_all_boards.delay(board)
    return {"message": "Crawling task has been triggered"}


@app.get("/clean")
def trigger_crawl_board():
    from db.crud import clean_tables
    clean_tables()
    return {"message": "Clean!"}
