
### 新人教育訓練： [FIRST_TRAINING.md](FIRST_TRAINING.md)

### 專案開發訓練：PTT WebServer

紀錄：專案架構、運作流程、資料格式、如何部屬、執行方式

#### 系統規劃

- 撰寫一個網站的爬蟲(每小時定時執行一次)，用資料庫(mariadb)儲存下來，透過撰寫 API 以及簡易的前端頁面進行呈現

- 運作流程圖
  > ![Flow.png](drawio-pic/Flow.png)

- 系統架構
  - project-file
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
      - static
        - index.html
      - api
        - ptt.py
      - main.py

- 資料表設計
  > ![ptt-database.png](img/ptt-database.png)


#### 專案呈現

- Tasks (爬蟲與排程)
  - PTT 五個版面的一年份資料，後續每小時爬取新資料
  - Celery
    - celery beat => 設定每小時一次的 "crawl-ptt-every-hour" schedule
  > ![celery-tasks.png](drawio-pic/celery-tasks.png)- 
  - PttCrawler
  > ![ptt-crawl.png](drawio-pic/ptt-crawl.png)

- API
  - 提供使用者方便操作資料庫的服務
  > ![api.png](img/api.png)
  > ![ptt-api.png](drawio-pic/ptt-api.png)

- 前端
  - 提供使用者操作介面，使用 js 呼叫 API 
  > ![ptt-web-frontend.png](img/ptt-web-frontend.png)
  > ![ptt-web-frontend-2.png](img/ptt-web-frontend-2.png)

- 部屬
  - docker-compose => 管理專案所使用到的各項服務(images -> containers)，方便轉移專案時能夠快速地再次建立相同的環境
  > ![deploy.png](drawio-pic/deploy.png)

