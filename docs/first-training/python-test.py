# 資料結構
# Set
the_set = {'A', 'B', 'C'}
print(f'theSet：{the_set}')
print(f'theSet：{the_set}')
# methods

# Set.add(subject)，將 subject 加入 Set 中
the_set.add("orange")
print(f'theSet.add("orange")：{the_set}')

# Set.remove(subject)，將 subject 從 Set 中移除
the_set.remove("orange")
print(f'theSet.remove("orange")：{the_set}')

# setA.union(setB), setA | setB
the_set_b = {'A', 'C', 'D'}
print(f'the_set_b：{the_set_b}')
print(f'the_set.union(the_set_b)：{the_set.union(the_set_b)}')

# setA.intersection(setB), setA & setB
print(f'the_set.intersection(the_set_b)：{the_set.intersection(the_set_b)}')

# setA.difference(setB), setA - setB
print(f'the_set.difference(the_set_b)：{the_set.difference(the_set_b)}')

# setA.symmetric_difference(setB), setA ^ setB
print(f'the_set.symmetric_difference(the_set_b)：{the_set.symmetric_difference(the_set_b)}')

print('=' * 50)

# List
the_list = ['A', 'B', 'C', 'A', 'B', 'C']
print(f'theList：{the_list}')

# Comprehension
second_list = [i for i in range(1, 11) if i % 2 == 0]
print(f'second_list：{second_list}')

print(f"theList[1]：{the_list[1]}")
print(f"theList[1:3]：{the_list[1:3]}")

# methods

# List.append(subject)，將 subject 從 List 末端加入 theList 中
the_list.append('Test')
print(f"theList.append('Test')：{the_list}")

# List.insert(index,subject)，將 subject 從 List[index] 加入 theList 中
the_list.insert(2, 'Test')
print(f"theList.insert(2, 'Test')：{the_list}")

# List.remove(subject)，將 subject 從 theList 中刪除，會從頭開始刪除第一個匹配到的
the_list.remove('Test')
print(f"theList.remove('Test')：{the_list}")

# List.pop(index)， 移除 List 中特定位置的元素，假如沒給定位置，則會移除最後一個元素，該方法最後會 return 被刪除的元素
print(f'theList.pop()，removed element：{the_list.pop()}，theList：{the_list}')

# List.reverse()，反轉 List 的順序
the_list.reverse()
print(f'theList.reverse()：{the_list}')


def my_function(subject):
    if subject == 'A':
        return 1
    elif subject == 'B':
        return 3
    elif subject == 'C':
        return 2
    return 0


# List.sort(reverse=False, key=myFunc)，對 List 排序，可由 reverse 選擇排序是否要反轉，可以自訂方法 myFunc 去決定排序的標準
the_list.sort()
print(f'theList.sort()：{the_list}')
the_list.sort(reverse=True)
print(f'theList.sort(reverse=True)：{the_list}')
the_list.sort(key=my_function)
print(f'theList.sort(key=myFunction)：{the_list}')

# List.index(subject)，subject 在 List 中從頭開始匹配，第一個匹配到的位置
print(f"theList.index('B')：{the_list.index('B')}")
# List.count(subject)，subject 在 List 中出現的次數
print(f"theList.count('B')：{the_list.count('B')}")

print('=' * 50)

# Tuple
the_tuple = ('A', 'B', 'C')
print(f'theTuple：{the_tuple}')

# methods

# Tuple.index(subject)，subject 在 Tuple 中從頭開始匹配，第一個匹配到的位置
print(f"theTuple.index('C')：{the_tuple.index('C')}")
# Tuple.count(subject)，subject 在 Tuple 中出現的次數
print(f"theTuple.count('C')：{the_tuple.count('C')}")

print('=' * 50)

# Dictionary
the_dict = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}

# Comprehension
second_dict = {f"{i}": i for i in range(1, 11) if i % 2 == 0}
print(f'theDict：{the_dict}')
print(f'second_dict：{second_dict}')

# Dict 快速存取值的寫法 => Dict[key]
# 沒有賦值便取出
print(f"theDict['A']：{the_dict['A']}")
# 若是舊的會改寫
the_dict['A'] = 'aa'
print(f"theDict['A']= 'aa'，theDict：{the_dict}")
# 若是新的會加入
the_dict['E'] = 'e'
print(f"the_dict['E'] = 'e'，theDict：{the_dict}")

# methods

# Dict.get(keyname, defaultValue)，return 由 keyname 索引到的 Dict 中的 value，defaultValue 會在該 keyname 索引不到 value 時 return
print(f"theDict.get('C')：{the_dict.get('C')}")

# Dict.items()，return 每一個 (key,value) 組成的 dict_item(List)
print(f"theDict.items()：{the_dict.items()}")

# Dict.keys()，return 每一個 key 組成的 dict_keys(List)
print(f"theDict.keys()：{the_dict.keys()}")

# Dict.values()，return 每一個 value 組成的 dict_values(List)
print(f"theDict.values()：{the_dict.values()}")

# Dict.pop(keyname, defaultValue)，移除由 keyname 索引到的 Dict 中的 value，
# 在方法最後 return 被刪除的 value，defaultValue 會在該 key 索引不到 value 時 return
print(f'theDict.pop()，removed value：{the_dict.pop('C')}，theDict：{the_dict}')

# Dict.popitem()，移除最後加入 Dict 的 key/value ，在方法最後 return 被刪除的 value
print(f'theDict.popitem()，removed value：{the_dict.popitem()}，theDict：{the_dict}')

print('=' * 50)

def test(a,b,c):
    print('')
test(b=1, 2)

# function
# *arg
def arg_function(*subject):
    return sum(subject)
    # print(f'arg_function(*subject)，subject：{subject}')
a=[1,2,3,4]
arg_function(*a)

arg_function(1, 1, 2, 3)
arg_function(1, 4)


# **kwargs
def kwargs_function(num1,**subject):
    print(f'kwargs_function(**subject)，subject：{subject}')


kwargs_function(num1=1, num2=2, num3=3)
kwargs_function(num1=1, num2=2, num3=3, num4=4)
print('=' * 50)


# yield
def yield_test(n):
    print(f'yield_test({n}) start')
    for i in range(n):
        print("i =", i)
        yield i * i
        # print("i =", i)

    print(f'yield_test({n}) end')


# 函數中有yield，所以該函數並不會真的執行，而是先得到一個生成器
yield_result = yield_test(5)
print(f'yield_result：{yield_result}')
for item in yield_result:
    print(f'yield_result，item：{item}')

yield_result = yield_test(5)
print("stop at item == 9")
for item in yield_result:
    if item == 9:
        break
    print(f'yield_result，item：{item}')

print('-' * 50)

yield_result = yield_test(5)
print('next(yield_result)')
print(next(yield_result))
print(next(yield_result))
print(next(yield_result))
print(next(yield_result))
print(next(yield_result))

print('=' * 50)


# Type Hint
def say_hi(name: str) -> str:
    return f'Hi {name}'


print("Type Hint")
greeting = say_hi('John')
print(greeting)
greeting = say_hi(123)
print(greeting)

print('=' * 50)

# Logging
import logging


def logging_method():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG, filename='logging-msg.log', filemode='w')
    logging.debug('Hello Debug')
    logging.info('Hello info')
    logging.warning('Hello WARNING')
    logging.error('Hello ERROR')
    logging.critical('Hello CRITICAL')

    try:
        llllllllogging.debug('Hello Debug')
    except Exception as e:
        logging.error("Catch an exception.", exc_info=True)


logging_method()

# load_dotenv
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 取得環境變數
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")

print(f".env")
print(f"Database URL: {database_url}")
print(f"API Key: {api_key}")
print(f"Debug Mode: {debug_mode}")
