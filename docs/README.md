
### 新人教育訓練： [FIRST_TRAINING.md](FIRST_TRAINING.md)

### 專案開發訓練：

紀錄：專案架構、運作流程、資料格式、如何部屬、執行方式

#### 系統規劃

- 系統架構
  - project-file
      - static
        - index.html
      - api
        - ppt_datacrawl.py
        - ppt.py
      - schema
        - ppt_content.py
      - model
        - ppt_content.py
      - db
        - base.py
      - main.py
- 資料表設計
  > ![資料表設計.png](img/%E8%B3%87%E6%96%99%E8%A1%A8%E8%A8%AD%E8%A8%88.png)
- 簡易前端設計
  > ![簡易前端設計.png](img/%E7%B0%A1%E6%98%93%E5%89%8D%E7%AB%AF%E8%A8%AD%E8%A8%88.png)
- 運作流程圖
  > ![運作流程圖.png](drawio-pic/%E9%81%8B%E4%BD%9C%E6%B5%81%E7%A8%8B%E5%9C%96.png)
- 規劃時程表
  > ![工作拆分與時程規劃-時間軸.png](img/%E5%B7%A5%E4%BD%9C%E6%8B%86%E5%88%86%E8%88%87%E6%99%82%E7%A8%8B%E8%A6%8F%E5%8A%83-%E6%99%82%E9%96%93%E8%BB%B8.png)

- 環境需求
  - 資料庫種類：mariadb
- 部屬方式
  - docker-compose