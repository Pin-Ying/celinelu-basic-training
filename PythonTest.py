### Set
theSet = set({'A', 'B', 'C'})
theSet = {'A', 'B', 'C'}
print(f'theSet：{theSet}')
print('-' * 50)

# methods

# Set.add(subject)，將 subject 加入 Set 中
theSet.add("orange")
print(f'theSet.add("orange")：{theSet}')
print('-' * 50)

# Set.copy()，會 return 一份複製的 Set
theSecondSet = theSet.copy()
print(f'theSecondSet = theSet.copy()，theSecondSet：{theSet}')
print(f'theSecondSet：{theSecondSet}')
print('-' * 50)

# Set.remove(subject)，將 subject 從 Set 中移除
theSet.remove("orange")
print(f'theSet.remove("orange")：{theSet}')
print('-' * 50)

# Set.clear()，將 Set 清空
theSet.clear()
print(f'theSet.clear()：{theSet}')
print('-' * 50)

print('=' * 50)

### List
theList = list(['A', 'B', 'C', 'A', 'B', 'C'])
theList = ['A', 'B', 'C', 'A', 'B', 'C']
print(f'theList：{theList}')
print('-' * 50)

# methods

# List.append(subject)，將 subject 從 List 末端加入 theList 中
theList.append(5566)
print(f'theList.append(5566)：{theList}')
print('-' * 50)

# List.insert(index,subject)，將 subject 從 List[index] 加入 theList 中
theList.insert(2, 5566)
print(f'theList.insert(2, 5566)：{theList}')
print('-' * 50)

# List.remove(subject)，將 subject 從 theList 中刪除，會從頭開始刪除第一個匹配到的
theList.remove(5566)
print(f'theList.remove(2, 5566)：{theList}')
print('-' * 50)

# List.pop(index)， 移除 List 中特定位置的元素，假如沒給定位置，則會移除最後一個元素，該方法最後會 return 被刪除的元素
print(f'theList.pop()，removed element：{theList.pop()}')
print(f'theList.pop()，theList：{theList}')
print('-' * 50)

# List.reverse()，反轉 List 的順序
theList.reverse()
print(f'theList.reverse()：{theList}')
print('-' * 50)


# List.sort(reverse=False, key=myFunc)，對 List 排序，可由 reverse 選擇排序是否要反轉，可以自訂方法 myFunc 去決定排序的標準
def myFunction(subject):
    if (subject == 'A'):
        return 1
    elif (subject == 'B'):
        return 3
    elif (subject == 'C'):
        return 2


theList.sort()
print(f'theList.sort()：{theList}')
theList.sort(reverse=True)
print(f'theList.sort(reverse=True)：{theList}')
theList.sort(key=myFunction)
print(f'theList.sort(key=myFunction)：{theList}')
print('-' * 50)

# List.index(subject)，subject 在 List 中從頭開始匹配，第一個匹配到的位置
print(f"theList.index('B')：{theList.index('B')}")
print('-' * 50)

# List.count(subject)，subject 在 List 中出現的次數
print(f"theList.count('B')：{theList.count('B')}")
print('-' * 50)

print('=' * 50)

### Tuple
theTuple = ('A', 'B', 'C')
print(f'theTuple：{theTuple}')
print('-' * 50)

# methods

# Tuple.index(subject)，subject 在 Tuple 中從頭開始匹配，第一個匹配到的位置
print(f"theTuple.index('C')：{theTuple.index('C')}")
print('-' * 50)

# Tuple.count(subject)，subject 在 Tuple 中出現的次數
print(f"theTuple.count('C')：{theTuple.count('C')}")
print('-' * 50)

print('=' * 50)

### Dictionary
theDict = dict({'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'})
theDict = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}
print(f'theDict：{theDict}')

# Dict 快速存取值的寫法 => Dic[key]
# 沒有賦值便取出
print(f"theDict['A']：{theDict['A']}")
# 若是舊的會改寫
theDict['A'] = 'aa'
print(theDict['A'])
# 若是新的會加入
theDict['E'] = 'e'
print(f'theDict<UNK>{theDict}')

print('-' * 50)

# methods

# Dict.get(keyname, defaultvalue)，return 由 keyname 索引到的 Dict 中的 value，defaultvalue 會在該 keyname 索引不到 value 時 return
print(f"theDict.get('C')：{theDict.get('C')}")
print('-' * 50)

# Dict.items()，return 每一個 (key,value) 組成的 List
print(f"theDict.items()：{theDict.items()}")
print('-' * 50)

# Dict.keys()，return 每一個 key 組成的 List
print(f"theDict.keys()：{theDict.keys()}")
print('-' * 50)

# Dict.values()，return 每一個 value 組成的 List
print(f"theDict.values()：{theDict.values()}")
print('-' * 50)

# Dict.pop(keyname, defaultvalue)，移除由 keyname 索引到的 Dict 中的 value，在方法最後 return 被刪除的 value，defaultvalue 會在該 key 索引不到 value 時 return
print(f'theDict.pop()，removed value：{theDict.pop('C')}')
print(f'theDict.pop()，theDict：{theDict}')
print('-' * 50)

# Dict.popitem()，移除最後加入 Dict 的 key/value ，在方法最後 return 被刪除的 value
print(f'theDict.popitem()，removed value：{theDict.popitem()}')
print(f'theDict.popitem()，theDict：{theDict}')
print('-' * 50)
