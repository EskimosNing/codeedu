# 快速排序算法的实现与测试

快速排序是一种高效的排序算法，采用分而治之的策略。算法基本步骤如下：

1. **选择基准**：从数组中选择一个基准元素，通常是中间的元素。
2. **分区**：将数组中的元素根据基准进行划分，分为三部分：
   - 小于基准的元素
   - 等于基准的元素
   - 大于基准的元素
3. **递归排序**：对小于基准和大于基准的子数组进行递归排序。
4. **合并结果**：将排序后的子数组与基准元素合并，得到最终排序的数组。

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]  # 选择数组的中间元素作为基准
    left = [x for x in arr if x < pivot]  # 小于基准的元素
    middle = [x for x in arr if x == pivot]  # 与基准相等的元素
    right = [x for x in arr if x > pivot]  # 大于基准的元素
    return quick_sort(left) + middle + quick_sort(right)  # 递归排序并合并

# 测试代码
if __name__ == '__main__':
    sample_array = [10, 7, 8, 9, 1, 5]
    sorted_array = quick_sort(sample_array)
    print('排序前:', sample_array)
    print('排序后:', sorted_array)
```

## 测试代码说明

在上述测试代码中，我们定义了一个示例数组 `sample_array`，其元素为 `[10, 7, 8, 9, 1, 5]`。运行该程序后，输出排序前后的数组来验证算法的正确性。

- **排序前**：`[10, 7, 8, 9, 1, 5]`
- **排序后**：`[1, 5, 7, 8, 9, 10]`

通过输出结果，可以清晰地看到快速排序算法成功地将数组从无序变为有序，为算法的有效性提供了直接验证。