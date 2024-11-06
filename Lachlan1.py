def binarySearch(array, target):
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = low + (low + high) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return "NONE"

arr6 = [1,2,4,6,7,9]
targetNum3 = 4
result = (binarySearch(arr6, targetNum3))
print("BinarySearch: Possition in array =", result)

