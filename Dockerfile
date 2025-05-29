FROM python:3.13-slim

# 安裝系統工具與 curl（給 poetry 用）
RUN apt-get update && apt-get install -y curl build-essential

# 安裝 Poetry 並加入 PATH
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 設定環境變數讓 Poetry 不建立虛擬環境（在容器中沒必要）
ENV POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 設定工作目錄
WORKDIR /app

# Poetry 建立環境
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

# 複製其他程式碼
COPY . .

# 預設指令可以在 docker-compose 裡覆蓋
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
