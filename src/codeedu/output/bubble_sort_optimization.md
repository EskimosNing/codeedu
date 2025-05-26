# 冒泡排序算法报告

## 1. 定义
冒泡排序（Bubble Sort）是一种基本的排序算法，它通过重复比较相邻元素并在必要时交换它们的顺序来排序。

## 2. 原理
- 从数组的第一个元素开始，逐个比较相邻的元素。
- 如果当前元素大于下一个元素，则交换它们的位置。
- 重复这个过程，直到整个数组有序。

## 3. 应用
冒泡排序适用于小规模数据的排序，简单易懂，但不适合大规模数据。

## 4. 优化建议
- **标志位优化**：如果没有交换，提前结束排序。
- **减少循环次数**：每完成一轮，下一轮可减少比较次数。

## 5. 时间复杂度
- 最坏和平均情况：O(n^2)
- 最好情况：O(n)（标志位优化）

## 6. 示例代码
```python

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
    return arr

if __name__ == "__main__":
    # 生成用例
    test_array = [64, 34, 25, 12, 22, 11, 90]
    sorted_array = bubble_sort(test_array)
    
    # 输出结果到 JSON 文件
    import json
    output = {"original": test_array, "sorted": sorted_array}

    with open('output/result.json', 'w') as json_file:
        json.dump(output, json_file)
```