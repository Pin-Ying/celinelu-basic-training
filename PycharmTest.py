# 執行變數設置： --x 1
import argparse

test_parser = argparse.ArgumentParser()
test_parser.add_argument("--x", type=int)
test_args = test_parser.parse_args()
# print 結果：1
print(test_args.x)

# 環境變數設置： VN_NAME=CoolBox
import os

# print 結果：CoolBox
print(os.getenv('VN_NAME'))


### Debug
# Run to cursor => Continues the execution until the position of the caret is reached.
# Step into => Enters the method to show what happens inside it.
# Step over => Steps over the current line of code and takes you to the next line even if the highlighted line has method calls in it.
# Step out => Steps out of the current method and takes you to the caller method.

def test_function(test_x, test_y):
    # 藉由 Step into 進入這行，Step into, Step over 都會跳到下一行， Step out 會跳回 z = test_function(x, y)
    num = test_x + test_y
    return num


num_x = 1
num_y = 2

# 於下方 z1 = num_x + num_y 設定 Line Breakpoint
# Step into, Step over, Step out 都會跳到下一行
z1 = num_x + num_y

# 於下方 z2 = test_function(num_x, num_y) 設定 Line Breakpoint
# Step into 會跳至定義 test_function 方法內部，Step over, Step out 會直接結束這行
z2 = test_function(num_x, num_y)

### Breakpoint
# 於下方 print(num_y) 該行設定 Line Breakpoint 的 Condition：y==2
# 結果：Resume Program 時會停下
print(num_y)

num_y = 3
# 於下方 print(num_y) 該行設定 Line Breakpoint 的 Condition：y==2
# 結果：Resume Program 時會直接跳過該點，因條件不符該點無啟用
print(num_y)

# 在 Python Exception Breakpoint 設置 ZeroDivisionError，並勾起 Log 中的 "Breakpoint hit" message
# Debug 結果：
# ZeroDivisionError: division by zero
# Breakpoint reached: ZeroDivisionError
# python-ZeroDivisionError
z3 = num_x / 0
