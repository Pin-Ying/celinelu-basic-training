
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

- 爬蟲
  - PttCrawler 類別
    - 抓取每一個 board 的方法皆相同
    - 抓取每一文章列表的方法皆相同
    - 抓取每篇文章的方法皆相同

  - Celery
    - Broker: Redis
    -
  - log
  > ![celery-log.png](img/celery-log.png)

- API
  > ![api.png](img/api.png)
- 前端
  > ![ptt-web-frontend.png](img/ptt-web-frontend.png)
  > ![ptt-web-frontend-2.png](img/ptt-web-frontend-2.png)
- 部屬
  - WebServer: Uvicorn
  - 
- 