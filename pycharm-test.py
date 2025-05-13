# 執行變數設置：
import argparse

test_parser = argparse.ArgumentParser()
test_parser.add_argument("--name")
test_parser.add_argument("--number", type=int)
test_args = test_parser.parse_args()

print(f"test_args.name: {test_args.name}")
print(f"test_args.number: {test_args.number}")

# 環境變數設置：
import os

print(f"os.getenv('VN_NAME'): {os.getenv('VN_NAME')}")

### Debug
# Resume Program 無論何時都是跳到下一個斷點

def test_function(test_x, test_y):
    # 藉由 Step into 進入這行
    # Step into, Step over 都會逐行執行
    # Step out 會跳到下一個斷點，直到離開方法時於該方法那行暫停
    num = test_x + test_y
    print(f"Test")
    print(f"Test")
    print(f"Test")
    return num


num_x = 1
num_y = 2

# 於下方 z1 = num_x + num_y 設定 Line Breakpoint
# Step into, Step over 逐行執行
# Step out 會跳到下一個斷點
z1 = num_x + num_y

print(f"Test")
print(f"Test")
print(f"Test")

# 於下方 z2 = test_function(num_x, num_y) 設定 Line Breakpoint
# Step into 會進入 test_function 方法內部逐行執行
# Step over 會嘗試直接執行完該行，但若方法內部有斷點則會暫停，並維持逐行執行
# Step out 會跳到下一個斷點，因此方法內部有斷點則會暫停
z2 = test_function(num_x, num_y)

print(f"Test")
print(f"Test")
print(f"Test")

### Breakpoint
# 於下方 print(num_y) 該行設定 Line Breakpoint 的 Condition：num_y==2
# 結果：Resume Program 時會停下
print(f"num_y: {num_y}")

num_y = 3
# 於下方 print(num_y) 該行設定 Line Breakpoint 的 Condition：num_y==2
# 結果：Resume Program 時會直接跳過該點，因條件不符該點無啟用
print(f"num_y: {num_y}")

# 在 Python Exception Breakpoint 設置 ZeroDivisionError，並勾起 Log 中的 "Breakpoint hit" message
# Debug 結果：
# ZeroDivisionError: division by zero
# Breakpoint reached: ZeroDivisionError
# python-ZeroDivisionError
z3 = num_x / 0

from mypackage import  mymodule
car = mymodule.Car()
