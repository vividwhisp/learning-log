def findMinMax(arr, start, end):
    if start == end:
        return arr[start], arr[end]

    if start + 1 == end:
        if arr[start] < arr[end]:
            return arr[start], arr[end]
        else:
            return arr[end], arr[start]

    mid = (start + end) // 2
    min1, max1 = findMinMax(arr, start, mid)
    min2, max2 = findMinMax(arr, mid+1, end)

    return min(min1, min2), max(max1, max2)

a = [64,32,25,50,45,40,51]
min, max = findMinMax(a, 0, len(a) - 1 )
print("Minimum: ", min)
print("Maximum: ", max)