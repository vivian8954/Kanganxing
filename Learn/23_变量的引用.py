a = 10
b= a
print('a',id(a))
print('b',id(b))

b = 20
print('a',id(a))
print('b',id(b))

list1 = [1, 2, 3]
print('list1',list1)
list1[1] = 9
print('list1',list1)

my_tuple = (1,3,[a, 4, b])
print(my_tuple)
my_tuple[-1][-1] = 9
print(my_tuple)