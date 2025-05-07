### Pycharm(IDE)

#### 部分功能補充在 PycharmTest.py

- 熟悉操作方式

    - 快捷鍵(Pycharm)：
        - Setting：ctrl+alt+s
        - 複製(若沒選擇字串則為一整行)：ctrl+c
        - 還原：ctrl+z
        - 重做：ctrl+shift+z
        - 刪除當前行(重做)：ctrl+y
        - 註解：ctrl+/
        - 縮排->：tab
        - 縮排<-：shift+tab
        - 重新命名(包括檔案、變數、方法)：shift+f6
        - 部分快捷鍵在後續作答中

- 執行程式的方式(一般執行)

    - 預設快捷鍵：shift+f10
  > ![run.png](img/run.png)

- 執行程式的方式(偵錯方式)

    - breakpoint：
        - What? => 程式執行時「達到特定條件則暫停」的斷點
        - Why? => 目的為檢查與確定程式是否按照設計的邏輯進行
        - How? (預設快捷鍵：ctrl+shift+f8)
        - Line Breakpoints：程式抵達到該行時暫停，在 Pycharm 中可以額外設定啟用條件(Condition)
        - Exception Breakpoints：程式丟出特定例外時暫停，可以此得知錯誤當下的資料狀態和鄰近的程式碼
  > ![breakpoint.png](img/breakpoint.png)
- 設定執行參數

    - What? => 執行程式時，隨著執行指令一同傳入的額外資訊
    - Why? => 接收從外部傳入的資料，根據條件不同進行不同的處理，增加程式使用靈活度
    - How? => 從 RUN 的面板 (預設快捷鍵：alt+4) 中，Modify Run Configuration 可以進行設定(如下圖)
  > ![modify-run-configuration.png](img/modify-run-configuration.png)
  > ![edit-run-configuration.png](img/edit-run-configuration.png)

- 快速尋找方法或參數的「源頭」或是「有哪些方法在使用」

    - 源頭：將輸入標放在要查詢的方法、參數上，點擊預設快捷鍵：ctrl+b，會自動跳到該項目的源頭位置

    - 有哪些方法在使用 => Find and replace，預設快捷鍵：ctrl+shift+f，可先將要尋找的字串選取再按快捷鍵

- 快速reformat程式碼：預設快捷鍵：ctrl+alt+l，可先將要 reformat 的程式碼選取後再按快捷鍵
    - 可以設定自動於儲存時 reformat
  > ![reformat-on-save.png](img/reformat-on-save.png)

### Python程式開發

虛擬環境操作

- 如何確認當前所在的虛擬環境為何?

    -

- requirements.txt

    - What? => 紀錄該 Python 專案需要的套件之文字檔
    - How? => 通常一行紀錄一個套件，為套件的名稱，若需要也可以加上套件的版本內容
    - Why? => 專案共用、發佈、轉移時，為方便快速建立專案環境，可以直接利用 requirements.txt 列出的套件確保專案一致性
