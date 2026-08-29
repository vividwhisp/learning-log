def selectionSort(a):
    n = len(a)

    for i in range(n):
        min = i
        for j in range(i, n):
            if a[min] < a[j]:
                min = j
        a[i], a[min] = a[min], a[i]

a= [64,32,25,50,45,40,51]
selectionSort(a)
print(a)