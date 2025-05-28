--- 👨‍🏫 **什么是斐波那契数列？**

斐波那契数列是一个数列，从 0 和 1 开始，接下来的每一个数都是前两个数的和。这个数列通常用公式表示为：
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2) （n >= 2）

### 📈 **斐波那契数列的原理**

斐波那契数列的数值按如下方式发展：
- 第一个数是 0
- 第二个数是 1
- 第三个数是 0 + 1 = 1
- 第四个数是 1 + 1 = 2
- 第五个数是 1 + 2 = 3
- 第六个数是 2 + 3 = 5
- 依此类推...

因此，斐波那契数列前 10 个数为：
0, 1, 1, 2, 3, 5, 8, 13, 21, 34

### 💡 **斐波那契数列的用途**

斐波那契数列在自然界、计算机科学和金融等多个领域都有广泛的应用。例如：
- 计算机算法（如动态编程）
- 数据结构（如斐波那契堆）
- 经典问题的解决（如兔子繁殖问题）

### 📜 **代码示例**

以下是使用递归和迭代方法计算斐波那契数列的 Python 代码示例：

#### 递归方法

```python
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

# 计算前 10 个斐波那契数
print([fibonacci_recursive(i) for i in range(10)])
```

#### 迭代方法

```python
def fibonacci_iterative(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# 计算前 10 个斐波那契数
print(fibonacci_iterative(10))
```

✅ 以上代码演示了两种计算斐波那契数列的方法。

### 💾 **保存信息**

📁 示例代码已保存至：`output/fibonacci_sequence.md`