def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]  # 选择中间的元素作为基准
        left = [x for x in arr if x < pivot]  # 小于基准的元素
        middle = [x for x in arr if x == pivot]  # 等于基准的元素
        right = [x for x in arr if x > pivot]  # 大于基准的元素
        return quick_sort(left) + middle + quick_sort(right)

# 示例使用
arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print(sorted_arr) 

# 快速排序是一种高效的排序算法，采用分治法策略。\n# 它的基本思想是选择一个基准元素，并将待排序的元素分为两部分：\n# 一部分是小于基准的元素，另一部分是大于基准的元素。\n# 然后对这两部分元素分别进行排序，最终将所有元素结合起来.
