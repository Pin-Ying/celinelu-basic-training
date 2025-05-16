from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# 掛載靜態資源資料夾
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 回傳 index.html 作為入口（例如 for React）
@app.get("/")
def read_index():
    return FileResponse("app/static/index.html")
