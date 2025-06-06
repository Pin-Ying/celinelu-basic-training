
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

- 環境需求
  - 資料庫種類：mariadb
- 部屬方式
  - docker-compose


#### 專案呈現

- Tasks (爬蟲與排程)
  - PttCrawler 類別 => 進行某個 Board 的文章爬取與資料庫儲存
    - crawl() => 爬取文章列表 -> 收集文章列表得到的文章a標籤，依序爬取單篇文章 -> 將爬取的文章收集，並從上頁按鈕進行下一頁的爬取 
      - 結束爬取條件：1.當單篇文章與前次最新的文章相同(前次終斷點)、2.批次抓取的文章中包含日期比 cutoff_date 舊的文章(沒有斷點文章時)
    - save_posts_from_postcrawls() => 將收集的文章存入資料庫

  - Celery
    - Broker: Redis
    - celery beat => 設定每小時一次的 "crawl-ptt-every-hour" schedule
    - crawl_all_boards() => 追蹤與整合不同 Borad 的爬取任務，並紀錄(log)任務開始、結束時間
  
  - log
  > ![celery-log.png](img/celery-log.png)

- API
  > ![api.png](img/api.png)
- 前端
  > ![ptt-web-frontend.png](img/ptt-web-frontend.png)
  > ![ptt-web-frontend-2.png](img/ptt-web-frontend-2.png)
- 部屬
  - Dockerfile
    - 使用 Poetry 建立環境
    - redis: celery broker、celery result backend
    - mariadb: database
    - web: web server(FastAPI + uvicorn)
    - celery_worker: run tasks
    - celery_beat: schedule tasks

