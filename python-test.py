### 資料結構
### Set
the_set = {'A', 'B', 'C'}
print(f'theSet：{the_set}')
print('-' * 50)

# methods

# Set.add(subject)，將 subject 加入 Set 中
the_set.add("orange")
print(f'theSet.add("orange")：{the_set}')
print('-' * 50)

# Set.copy()，會 return 一份複製的 Set
theSecondSet = the_set.copy()
print(f'theSecondSet = theSet.copy()，theSecondSet：{the_set}')
print(f'theSecondSet：{theSecondSet}')
print('-' * 50)

# Set.remove(subject)，將 subject 從 Set 中移除
the_set.remove("orange")
print(f'theSet.remove("orange")：{the_set}')
print('-' * 50)

# Set.clear()，將 Set 清空
the_set.clear()
print(f'theSet.clear()：{the_set}')
print('-' * 50)

print('=' * 50)

### List
the_list = ['A', 'B', 'C', 'A', 'B', 'C']
print(f'theList：{the_list}')
print('-' * 50)

# methods

# List.append(subject)，將 subject 從 List 末端加入 theList 中
the_list.append('Test')
print(f'theList.append(5566)：{the_list}')
print('-' * 50)

# List.insert(index,subject)，將 subject 從 List[index] 加入 theList 中
the_list.insert(2, 'Test')
print(f'theList.insert(2, 5566)：{the_list}')
print('-' * 50)

# List.remove(subject)，將 subject 從 theList 中刪除，會從頭開始刪除第一個匹配到的
the_list.remove('Test')
print(f'theList.remove(2, 5566)：{the_list}')
print('-' * 50)

# List.pop(index)， 移除 List 中特定位置的元素，假如沒給定位置，則會移除最後一個元素，該方法最後會 return 被刪除的元素
print(f'theList.pop()，removed element：{the_list.pop()}')
print(f'theList.pop()，theList：{the_list}')
print('-' * 50)

# List.reverse()，反轉 List 的順序
the_list.reverse()
print(f'theList.reverse()：{the_list}')
print('-' * 50)


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
print('-' * 50)

# List.index(subject)，subject 在 List 中從頭開始匹配，第一個匹配到的位置
print(f"theList.index('B')：{the_list.index('B')}")
print('-' * 50)

# List.count(subject)，subject 在 List 中出現的次數
print(f"theList.count('B')：{the_list.count('B')}")
print('-' * 50)

print('=' * 50)

### Tuple
the_tuple = ('A', 'B', 'C')
print(f'theTuple：{the_tuple}')
print('-' * 50)

# methods

# Tuple.index(subject)，subject 在 Tuple 中從頭開始匹配，第一個匹配到的位置
print(f"theTuple.index('C')：{the_tuple.index('C')}")
print('-' * 50)

# Tuple.count(subject)，subject 在 Tuple 中出現的次數
print(f"theTuple.count('C')：{the_tuple.count('C')}")
print('-' * 50)

print('=' * 50)

### Dictionary
the_dict = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}
print(f'theDict：{the_dict}')

# Dict 快速存取值的寫法 => Dic[key]
# 沒有賦值便取出
print(f"theDict['A']：{the_dict['A']}")
# 若是舊的會改寫
the_dict['A'] = 'aa'
print(the_dict['A'])
# 若是新的會加入
the_dict['E'] = 'e'
print(f'theDict<UNK>{the_dict}')

print('-' * 50)

# methods

# Dict.get(keyname, defaultValue)，return 由 keyname 索引到的 Dict 中的 value，defaultValue 會在該 keyname 索引不到 value 時 return
print(f"theDict.get('C')：{the_dict.get('C')}")
print('-' * 50)

# Dict.items()，return 每一個 (key,value) 組成的 List
print(f"theDict.items()：{the_dict.items()}")
print('-' * 50)

# Dict.keys()，return 每一個 key 組成的 List
print(f"theDict.keys()：{the_dict.keys()}")
print('-' * 50)

# Dict.values()，return 每一個 value 組成的 List
print(f"theDict.values()：{the_dict.values()}")
print('-' * 50)

# Dict.pop(keyname, defaultValue)，移除由 keyname 索引到的 Dict 中的 value，在方法最後 return 被刪除的 value，defaultValue 會在該 key 索引不到 value 時 return
print(f'theDict.pop()，removed value：{the_dict.pop('C')}')
print(f'theDict.pop()，theDict：{the_dict}')
print('-' * 50)

# Dict.popitem()，移除最後加入 Dict 的 key/value ，在方法最後 return 被刪除的 value
print(f'theDict.popitem()，removed value：{the_dict.popitem()}')
print(f'theDict.popitem()，theDict：{the_dict}')
print('-' * 50)

print('=' * 50)


### function
### *arg
def arg_function(*subject):
    print(f'arg_function，subject：{subject}')


arg_function(1, 1, 2, 3)
arg_function(1, 4)


### **kwargs
def kwargs_function(**subject):
    print(f'kwargs_function，subject：{subject}')


kwargs_function(num1=1, num2=2, num3=3)
kwargs_function(num1=1, num2=2, num3=3, num4=4)
print('-' * 50)


### yield
def yield_test(n):
    print("start n =", n)
    for i in range(n):
        yield i * i
        print("i =", i)

    print("end")


yield_result = yield_test(1)
print(yield_result)
for item in yield_result:
    print(item)


### Type Hint
def say_hi(name: str) -> str:
    return f'Hi {name}'


greeting = say_hi('John')
# greeting = say_hi(123)
print(greeting)

### Logging
import logging


def main():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG, filename='test.log', filemode='w')
    logging.debug('Hello Debug')
    logging.info('Hello info')
    logging.warning('Hello WARNING')
    logging.error('Hello ERROR')
    logging.critical('Hello CRITICAL')

    try:
        llllllllogging.debug('Hello Debug')  # 定義錯誤
    except Exception as e:
        # logging.error("Catch an exception.", exc_info=True)
        logging.error("Catch an exception.")


main()

### load_dotenv
from dotenv import load_dotenv
import os

# 載入 .env 檔案
load_dotenv()

# 取得環境變數
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
debug_mode = os.getenv("DEBUG")

print(f"Database URL: {database_url}")
print(f"API Key: {api_key}")
print(f"Debug Mode: {debug_mode}")
