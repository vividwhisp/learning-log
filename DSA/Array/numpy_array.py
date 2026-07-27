from numpy import *
#heterogenous array

val = array([1,2,3,4.5,'a'])

zero = array(10)
print(zero)

one = array([1,2,3,4])
print(one)

two = array([[1,2,3],[4,5,6]])
print(two)

threed = array([[[1,23] , [1,2]],
                [[1,4] , [8,9]]])
print(threed)
#threed should be homogenous


# val = linspace(10,50,5)

# val = arange(10,20,2)

# val = logspace(10,20,2)

# val = zeros(10)

# val = ones(10)

# val = full(10,5)

# for x in val:
#     print(x, end=" ")