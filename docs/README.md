
### 新人教育訓練： [FIRST_TRAINING.md](FIRST_TRAINING.md)

### 專案開發訓練：

紀錄：專案架構、運作流程、資料格式、如何部屬、執行方式

#### 系統規劃

- 系統架構
  - project-file
      - static
        - index.html
      - api
        - ppt.py
      - schema
        - ppt_content.py
      - model
        - ppt_content.py
      - db
        - base.py
      - tasks
        - celery_tasks.py
        - ptt_crawl.py
      - tests
        - test_crud.py
        - test_ptt_crawl.py
      - main.py

- 資料表設計
  > ![ptt-web-server.png](img/ptt-web-server.png)
- 前端初期設計
  > ![frontEnd-design.png](img/frontEnd-design.png)
  
- 運作流程圖
  > ![運作流程圖.png](drawio-pic/%E9%81%8B%E4%BD%9C%E6%B5%81%E7%A8%8B%E5%9C%96.png)
- 規劃時程表
  > ![工作拆分與時程規劃-時間軸.png](img/%E5%B7%A5%E4%BD%9C%E6%8B%86%E5%88%86%E8%88%87%E6%99%82%E7%A8%8B%E8%A6%8F%E5%8A%83-%E6%99%82%E9%96%93%E8%BB%B8.png)

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
- 排程
  - Celery
- API
- 測試
- 前端
  > ![ptt-web-frontend.png](img/ptt-web-frontend.png)
  > ![ptt-web-frontend-2.png](img/ptt-web-frontend-2.png)
- 部屬
  - WebServer：Uvicorn