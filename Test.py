# Debug
# Breakpoints
# Line breakpoints => 設定程式該於抵達哪段程式碼時暫停，任一行程式碼都可以設定
# Exception breakpoints => 設定程式該於哪些異常發生時暫停
# Run to cursor => Continues the execution until the position of the caret is reached.
# Step into => Enters the method to show what happens inside it.
# Step over => Steps over the current line of code and takes you to the next line even if the highlighted line has method calls in it.
# Step out => Steps out of the current method and takes you to the caller method.

# 用於取得執行變數
import argparse
# 用於取得環境變數
import os

# x=1
y = 2

test_parser = argparse.ArgumentParser()
test_parser.add_argument("--x", type=int)
test_args = test_parser.parse_args()


def test_function(test_x, test_y):
    if test_x == 1 and test_y == 2:
        return test_x * y
    return 0


print(os.getenv('VN_NAME'))
print(test_args.x)
print(y)

z = test_args.x + y
print(z)
z2 = test_function(test_args.x, y)

print(z2)
print(z / 1)
print(z / z2)
