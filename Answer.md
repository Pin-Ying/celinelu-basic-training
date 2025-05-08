### Pycharm(IDE)

#### 部分功能補充在 PycharmTest.py

- 熟悉操作方式
    - 建立新 Python 專案 => File -> New Project
        - Interpreter type => 主要差異為 environment manager (conda, poetry...等等)
  > ![creat-new-project.png](img/creat-new-project.png)

    - 新增檔案(e.g. Python File)
        - 在欲新增檔案的資料夾上右鍵 -> New -> Python File 或其他欲加入的檔案
  > ![add-new-file.png](img/add-new-file.png)

    - 程式碼編寫
        - 快捷鍵(Pycharm)：
            - 複製並貼上該行：ctrl+d
            - 刪除當前行(重做)：ctrl+y
            - 註解：ctrl+/
            - 縮排->：tab
            - 縮排<-：shift+tab
            - 重新命名(包括檔案、變數、方法)：shift+f6

    - 設定 (預設快捷鍵：ctrl+alt+s) => 與 Pycharm 相關的設定，包括運行專案的環境
        - Project：該專案所處環境設置，包括 Python interpreter、Project Structure
  > ![setting.png](img/setting.png)


- 執行程式的方式(一般執行) => 一般測試程式時
    - 預設快捷鍵：shift+f10
    - 執行結果將會顯示在 Run 的面板 (預設快捷鍵：alt+4) ，包括程式執行結果、錯誤訊息
  > ![run.png](img/run.png)
  > ![run-result.png](img/run-result.png)

- 執行程式的方式(偵錯方式) => 當遇到較複雜、不易解決的錯誤時(e.g. 邏輯型錯誤)，針對可能造成錯誤的程式區塊進行測試，以利找到問題的源頭
    - 預設快捷鍵：shift+f9
    - 執行過程中，運行當下的資料內容(變數)將會顯示在 Debug 的面板 (預設快捷鍵：alt+5) 的 Threads & Variables
    -
  > ![run-debug.png](img/run-debug.png)
  > ![run-debug-debugging.png](img/run-debug-debugging.png)
    - 下圖借用了 PyCharm 官方文件圖來說明
  > ![debug-window.png](https://resources.jetbrains.com/help/img/idea/2025.1/py_debug_tool_window_dark.png)

    - Debugger toolbar (官方圖中的第5項) => Debug 過程中控制程式碼流程，透過這列工具決定哪幾段程式會被檢查
        - 可自行調整各功能擺放位置(工具列上按右鍵，Customize Toolbar)
        - Rerun 'TheTest'：重新跑一次 Debug
        - Stop 'TheTest'：直接終止執行中的程式
        - Resume Program：點此將暫停執行的程式恢復運行
        - Pause Program：手動暫停執行中的程式，會在當下正在執行的那段停下(可能使用場景 e.g. 程式運行過久、無限迴圈)
        - Step Over：執行當行程式碼，但遇到該行程式碼中使用的方法，不會進入方法 Reference，直接執行至下行
        - Step Into：執行當行程式碼，並在遇到方法時，進入方法 Reference 執行
            - Step Into My Code：與 Step Into 差異在不會進入函式庫(當遇到在函式庫的方法時不會進入)，只會停留在自己的程式碼中
        - Step Out：當目前正在方法 Reference 中時，跳出方法並回到該方法被執行那行

    - Threads & Variables
        - Threads => 執行續，在這裡會根據選擇的執行續，顯示執行續正暫停在程式碼的哪個區域位置
        - Variables => 變數，在這裡會根據選擇的執行續與區域位置，顯示該區域的變數
            - Evaluate expression (Enter)：根據輸入的表達式(e.g. 一個變數)回應 Result
              => ![evaluate-expression.png](img/evaluate-expression.png)
            - add a watch (Ctrl+Shift+Enter)：有時程式碼較為複雜，可利用此功能追蹤想知道的內容(表達式)
              => ![add-a-watch.png](img/add-a-watch.png)
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
    - How? => 從 Run 的面板中，Modify Run Configuration 可以進行設定(如下圖)
  > ![modify-run-configuration.png](img/modify-run-configuration.png)
  > ![run-configuration.png](img/run-configuration.png)

- 快速尋找方法或參數的「源頭」或是「有哪些方法在使用」
    - 源頭：將輸入標放在要查詢的方法、參數上，點擊預設快捷鍵：ctrl+b，會自動跳到該項目的源頭位置
    - 有哪些方法在使用 => Find and replace，預設快捷鍵：ctrl+shift+f，可先將要尋找的字串選取再按快捷鍵

- 快速reformat程式碼：預設快捷鍵：ctrl+alt+l，可先將要 reformat 的程式碼選取後再按快捷鍵
    - 可以設定自動於儲存時 reformat
  > ![reformat-on-save.png](img/reformat-on-save.png)

### Python程式開發

- 虛擬環境操作
    - 虛擬環境：
        - What? =>
        - Why? => 獨立的環境下，讓各專案在開發時套件獨立而互不衝突

    - 如何確認當前所在的虛擬環境為何?
        - 在虛擬環境 activate 的情況下，終端上會在當下目錄前提示目前所在的虛擬環境：(VENV_NAME)
  > ![terminal-venv.png](img/terminal-venv.png)

    - requirements.txt 的意義為何，如何建立與使用
        - What? => 紀錄該 Python 專案需要的套件之文字檔
        - Why? => 專案共用、發佈、轉移時，為方便快速建立專案環境，可以直接利用 requirements.txt 列出的套件確保專案一致性
        - How? => 通常一行紀錄一個套件，為套件的名稱，若需要也可以加上套件的版本(用==分隔套件名與版本號，e.g.
          Django==5.1.1)
            - 可以手動於專案目錄建立，也可以使用 pip freeze 將當下環境的套件寫成 requirements.txt => pip freeze >
              requirements.txt
            - 可以使用 pip 安裝檔案中的套件 => pip install -r requirements.txt

- python基本練習
    - 如何執行一隻 python 程式
        - 從終端接收要求，決定要執行哪支程式(e.g. 透過命令列下指令：> python3 file.py)
        - 進到 Python 直譯器(interpreter) => 負責翻譯 Python 腳本(.py檔案)，將內容轉換為位元組碼(Byte Code)
            - Byte Code：執行過渡期產生的 Code，因其方便轉換，能跨平台、系統對接，省去重複編譯的步驟
        - 進到 Virtual Machine => 負責將接收的 Byte Code 解析成 Machine Code, Executable Code
        - 觸發 CPU 和其他系統去執行任務

    - 資料結構
        - Set
            - What? => 無序、不允許重複元素的資料結構
            - When? => 當只需保留資料種類，且與資料次序無關時使用
            - Where? =>
        - List (*Comprehension)
            - What? => 有序、可變、可重複元素的資料結構
            - When? => 當需保留以資料次序作為索引的資料集合，且資料需保留修改的靈活度時使用
            - Where? =>
        - Tuple
            - What? => 有序、不可變、可重複元素的資料結構
            - When? => 當需保留以資料次序作為索引的資料集合，且無修改資料需求時使用
            - Where? =>
        - Dictionary(*Comprehension)
            - What? => 無序、可變、鍵值對應的資料結構
            - When? => 當處理資料中具非資料次序之索引資料(key)，需保留其索引關係時使用
            - Where? =>

    - function
        - Positional Arguments(*args) 與 Keyword Arguments(**kwargs)
        - return 與 yield
        - Type Hints

    - Package及Module
        - 如何引用套件與使用套件
        - `if __name__ == '__main__'`的意義為何

    - 環境變數如何設定與讀取(從IDE、python-dotenv設定)
