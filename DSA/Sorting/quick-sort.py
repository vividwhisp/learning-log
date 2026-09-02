def quickSort(arr, l, r):
    if(l<r):
       p = partition(arr, l, r)
       quickSort(arr, l, p-1)
       quickSort(arr, p+1, r)

    


def partition(arr, l, r):
    pivot = arr[l]
    i = l + 1
    j = r

    while True:
        while i < j and arr[i] < pivot:
            i += 1
        while i < j and arr[j] > pivot:
            j -= 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else: 
            break

    arr[l], arr[j] = arr[j], arr[l] 

    return j

a = [64,32,25,50,45,40,51]
quickSort(a, 0, len(a) - 1)
print(a)


    
    