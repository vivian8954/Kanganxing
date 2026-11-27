"""
函数的传参方式
"""
def func(a, b, c):
    print(f'a:{a}, b:{b}, c:{c}')

# 位置传参
func(1, 2, 3)
# 关键字传参
func(a=3, c=1, b=2)
# 混合传参
func(1, c=2, b=3)

"""
缺省参数，默认传参
"""
def info(name, age=18, sex='male'):
    print(f'name:{name}, age:{age}, sex:{sex}')
    print('------------------')
info('Alice')
info('Bob', 20)
info('Charlie', sex='female')

"""
多值参数，可变参数
"""
def add(a, *args, c = 100):
    print(f'a:{a}, args:{args}, c:{c}')
    print(type(args))
add(1)
add(1, 2, 3)
add(1, 2, 3, 4, 5, 6)
add(1, 2, 3, 4, 5, c =2)
add(1, c = 2)
