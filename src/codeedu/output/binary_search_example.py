# 二分查找算法示例

## 📘 什么是二分查找算法？

二分查找（Binary Search）是一种高效的查找算法，适用于在一个已经排序的数组中查找特定元素。它的基本原理是每次将搜索范围缩小一半，直到找到目标元素为止。其时间复杂度为 O(log n)，比线性查找算法 O(n) 高效得多。

## 💡 原理

1. **输入**：一个已排序的数组和一个目标值。
2. **过程**：
   - 找到数组的中间元素。
   - 如果中间元素等于目标值，则查找成功。
   - 如果目标值小于中间元素，则在左半部分继续查找。
   - 如果目标值大于中间元素，则在右半部分继续查找。
3. **输出**：目标值的索引或 -1（表示未找到）。

## 🔍 用途

二分查找广泛应用于各种场景，如：
- 在有序数据集中快速查找元素。
- 在处理大规模数据时，减少查找时间。

## 📄 Python代码示例

下面是一个示例实现：

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid  # 找到目标值，返回索引
        elif arr[mid] < target:
            left = mid + 1  # 在右半部分继续查找
        else:
            right = mid - 1  # 在左半部分继续查找
    return -1  # 未找到目标值

# 使用示例
if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    target = 5
    result = binary_search(numbers, target)
    if result != -1:
        print(f'元素 {target} 的索引为: {result}')
    else:
        print('未找到元素。')
```

✅ 以上代码演示了如何在已排序的数组中实现二分查找。
📁 示例代码已保存至：`output/binary_search_example.py`