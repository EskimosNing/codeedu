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