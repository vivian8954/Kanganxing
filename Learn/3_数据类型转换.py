"""
    input函数得到的数据都是字符串类型
"""
age = input('请输入你的年龄：')

print('1.您所输入的年龄是：', age, '数据类型为：', type(age))
new_age = int(float(age))  # 转换成了int类型
print('2.int转换后是：', new_age, '数据类型为：', type(new_age))
new_age2 = float(age)  # 转换成了int类型
print('3.float转换后是：', new_age2, '数据类型为：', type(new_age2))
