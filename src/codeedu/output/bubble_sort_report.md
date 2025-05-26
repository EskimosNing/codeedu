# 冒泡排序报告

## 1. 引言
冒泡排序是一种简单的排序算法，通过重复地遍历待排序列，比较每对相邻元素，如果它们的顺序错误就把它们交换过来。遍历工作是重复进行的，直到没有再需要交换的情况为止，这意味着该列表已经排序完成。

## 2. 代码实现
下面是冒泡排序的 Python 实现：

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

if __name__ == '__main__':
    test_cases = [[64, 34, 25, 12, 22, 11, 90], [5, 1, 4, 2, 8], [3, 0, 2, 5, -1, 4, 1]]
    results = {}
    for case in test_cases:
        sorted_case = bubble_sort(case)
        results[str(case)] = sorted_case
    print(results)
```

## 3. 时间复杂度分析
- **最坏情况**: O(n^2)
- **最好情况**: O(n)（当数组已经有序时）
- **平均情况**: O(n^2)

## 4. 空间复杂度分析
冒泡排序的空间复杂度为 O(1)，因为它是原地排序，不需要额外的存储空间。

## 5. 优化方法
在原始冒泡排序中，我们可以使用一个标志位，判断在某一趟中是否有交换，如果没有交换则说明数组已经有序，可以提前退出循环，降低运行时间。