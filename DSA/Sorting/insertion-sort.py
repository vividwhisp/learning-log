def insrtionSort(a):
    n = len(a)

    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j>=0 and key > a[j]:
            a[j+1] = a[j]
            j = j - 1

        a[j+1] = key

a= [64,32,25,50,45,40,51]
insrtionSort(a)
print(a)