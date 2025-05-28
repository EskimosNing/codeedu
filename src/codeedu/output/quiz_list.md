# 编程练习题集

## ✅ 题目 1 - 编程题
### ❓ 题目描述
实现一个函数 `is_palindrome(s: str) -> bool`，判断给定的字符串是否是回文字符串（正着读和反着读都相同的字符串）。

### 💬 示例输入与输出
- 示例输入：`"racecar"`  
  示例输出：`True`  
- 示例输入：`"hello"`  
  示例输出：`False`  

### 🧠 简要答案与解析
可以通过将字符串反转并与原字符串比较，来检查是否为回文。实现时需要注意忽略大小写及空格。

```python
def is_palindrome(s: str) -> bool:
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```

---

## ✅ 题目 2 - 编程题
### ❓ 题目描述
编写函数 `fibonacci(n: int) -> List[int]`，生成前 `n` 个斐波那契数。

### 💬 示例输入与输出
- 示例输入：`5`  
  示例输出：`[0, 1, 1, 2, 3]`  
- 示例输入：`8`  
  示例输出：`[0, 1, 1, 2, 3, 5, 8, 13]`  

### 🧠 简要答案与解析
斐波那契数列的定义是前两个数之和等于第三个数。可以通过循环或递归实现这一过程。

```python
from typing import List

def fibonacci(n: int) -> List[int]:
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]
```

---

## ✅ 题目 3 - 编程题
### ❓ 题目描述
编写函数 `sort_array(arr: List[int]) -> List[int]`，对给定的整数数组进行升序排序。

### 💬 示例输入与输出
- 示例输入：`[5, 2, 9, 1, 5, 6]`  
  示例输出：`[1, 2, 5, 5, 6, 9]`  
- 示例输入：`[3, 0, 2, 8, 6]`  
  示例输出：`[0, 2, 3, 6, 8]`  

### 🧠 简要答案与解析
可以使用 Python 的内置排序函数或实现一个排序算法（如冒泡排序）。以下是使用内置函数的示例。

```python
from typing import List

def sort_array(arr: List[int]) -> List[int]:
    return sorted(arr)
```

---

## ✅ 题目 4 - 编程题
### ❓ 题目描述
实现函数 `count_vowels(s: str) -> int`，统计字符串中元音字母的个数（元音字母为：a, e, i, o, u）。

### 💬 示例输入与输出
- 示例输入：`"hello world"`  
  示例输出：`3`  
- 示例输入：`"Python"`  
  示例输出：`1`  

### 🧠 简要答案与解析
可以通过遍历字符串，检查每个字符是否为元音字母并计数。

```python
def count_vowels(s: str) -> int:
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)
```

---

## ✅ 题目 5 - 编程题
### ❓ 题目描述
编写函数 `merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]`，将两个已排序的数组合并为一个新的排序数组。

### 💬 示例输入与输出
- 示例输入：`[1, 3, 5]`, `[2, 4, 6]`  
  示例输出：`[1, 2, 3, 4, 5, 6]`  
- 示例输入：`[0, 2, 4]`, `[1, 3, 5]`  
  示例输出：`[0, 1, 2, 3, 4, 5]`  

### 🧠 简要答案与解析
可以利用双指针的方法遍历两个数组，逐步构建合并后的数组。

```python
from typing import List

def merge_sorted_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result
```

---

📁 练习题已保存至：`output/quiz_list.md`   📥 点击下载查看完整题目与答案。