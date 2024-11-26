from itertools import chain

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]

tot = list(chain(a, b, c))
print(tot)

nested_loop = [[1, 2, 3], [4, 5, 6]]
another_nested_loop = [["a", "b", "c"]]

print(list(chain(*nested_loop, *another_nested_loop)))


a = [[[1,2,3],[4,5,6]]]
b = [[1,2,3]]

print(list(chain(*a, *b)))