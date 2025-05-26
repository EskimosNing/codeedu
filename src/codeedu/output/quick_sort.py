# 快速排序

## 定义
快速排序（Quicksort）是一种高效的排序算法，采用分治法（Divide and Conquer）策略，将一个数组分为两个子数组，分别对这两个子数组进行递归排序。

## 原理
1. 选择一个基准元素（pivot），通常选择数组的中间元素。
2. 分割数组，将小于基准元素的所有元素放在左边，大于基准元素的放在右边。
3. 递归地对左右两个子数组进行排序。
4. 合并左右两个已排序的子数组和基准元素，形成排序后的数组。

## 应用
快速排序广泛应用于数据处理领域，尤其是在需要高效排序的场景，如搜索引擎、数据库管理系统等。

## Python 实现
以下是快速排序的 Python 实现：

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 测试快速排序函数
if __name__ == '__main__':
    sample_array = [3, 6, 8, 10, 1, 2, 1]
    sorted_array = quick_sort(sample_array)
    print('原数组:', sample_array)
    print('排序后的数组:', sorted_array) 

# 该脚本包含了快速排序的 Python 实现，并通过测试展示了排序功能。