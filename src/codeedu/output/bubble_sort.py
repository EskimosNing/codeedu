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