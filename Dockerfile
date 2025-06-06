FROM python:3.13-slim

# 安裝系統工具與 curl（安裝 poetry 用）
RUN apt-get update && apt-get install -y curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Poetry 並加入 PATH
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 設定環境變數
# ENV POETRY_VIRTUALENVS_CREATE=false => Poetry 不自動建立虛擬環境(容器中不需要)
# ENV PYTHONUNBUFFERED=1 => Python 的 log 輸出不使用緩衝區，即時輸出 log
# ENV PYTHONDONTWRITEBYTECODE=1 => 不要寫入 .pyc 檔案（Python 執行暫存檔）
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 設定工作目錄
WORKDIR /app

# Poetry 建立環境
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# 複製當前目錄的所有檔案到容器的 /app
COPY . .

# 預設容器啟動時執行的指令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
