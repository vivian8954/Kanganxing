# 1．定义一个匿名函数，求两个数的乘积(两个参数)
# 2.定义一个匿名函数，获取字典中 键为age对应的值(参数一个字典)
def multi(a, b):
    return a * b

print(multi(3, 4))
# 2.定义一个匿名函数，获取字典中 键为age对应的值(参数一个字典)
def get_age(my_dict):
    return my_dict['age']
print(get_age({'name': 'zhangsan', 'age': 18}))



print((lambda a, b: a + b)(3, 4))

num = lambda a, b: a * b
print('定义一个匿名函数，求两个数的乘积', num(3, 4))

get_age = lambda x: x.get('age')
print('定义一个匿名函数，获取字典中 键为age对应的值', get_age({'name': 'zhangsan', 'age': 18}))

uesr_list = [
    {'name': 'zhangsan', 'age': 18},
    {'name': 'lisi', 'age': 24},
    {'name': 'wangwu', 'age': 22}
]
uesr_list.sort(key=lambda x: x['age'])
print(uesr_list)
uesr_list.sort(key=lambda x: x['age'], reverse=True)
print(uesr_list)