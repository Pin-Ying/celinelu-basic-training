
### 新人教育訓練： [FIRST_TRAINING.md](FIRST_TRAINING.md)

### 專案開發訓練：PTT WebServer

紀錄：專案架構、運作流程、資料格式、如何部屬、執行方式

#### 系統規劃

- 系統架構
  - project-file
      - static
        - index.html
      - api
        - ptt.py
      - schema
        - ptt_content.py
      - model
        - ptt_content.py
      - db
        - database.py
        - crud.py
      - tasks
        - celery_tasks.py
        - ptt_crawl.py
      - tests
        - test_crud.py
        - test_ptt_crawl.py
      - main.py

- 資料表設計
  > ![ptt-database.png](img/ptt-database.png)
- 前端初期設計
  > ![frontEnd-design.png](img/frontEnd-design.png)
  
- 運作流程圖
  > ![Flow.png](drawio-pic/Flow.png)
- 規劃時程表
  > ![schedule.png](img/schedule.png)
- 部屬方式
  - docker-compose


#### 專案呈現

- Tasks (爬蟲與排程)
  - PttCrawler
  > ![ptt-crawl.png](drawio-pic/ptt-crawl.png)

  - Celery
    - Broker: Redis
    - celery beat => 設定每小時一次的 "crawl-ptt-every-hour" schedule
  > ![celery-tasks.png](drawio-pic/celery-tasks.png)
  
  - log
  > ![celery-log.png](img/celery-log.png)

- API
  > ![api.png](img/api.png)
- 前端
  > ![ptt-web-frontend.png](img/ptt-web-frontend.png)
  > ![ptt-web-frontend-2.png](img/ptt-web-frontend-2.png)
- 部屬
  - docker-compose.yml
    - redis: celery broker、celery result backend
    - mariadb: database
    - images build by Dockerfile
      - web: web server(FastAPI + uvicorn)
      - celery_worker: run tasks
      - celery_beat: schedule tasks
  - Dockerfile
    - 使用 Poetry 建立環境

