# 1．提示用户输入用户姓名，并保存到变量中-->input
name = input('请输入姓名：')
# 2，提示用户输入用户年龄，保存到变量中，并转换成整数
age = input('请输入年龄:')  # str
age = int(age)
# 3，提示用户输入用户身高，保存到变量中，并转换成浮点数
height = float(input('请输入身高:'))
# 4，在控制台输出用户姓名、年龄、身高对应变量的数据类型
print(type(name), type(age), type(height))
# 5.按照以下格式输出用户信息：“姓名：xxx年龄：xxx身高：xxx”
print(f'姓名:{name}，年龄:{age}，身高:{height}')
print('姓名: {}，年龄:{}， 身高:{}'.format(name, age, height))
# 6，在控制台输出该用户5年之后的年龄，格式：“张三5年之后的年龄是25”
print(f'{name}15年之后的年龄是{age + 15}')
# 7，在控制台输出该用户现在是否成年，格式：“张三是否成年：True”
print(f'{name}是否成年:{age>=18}')
print(f'{name}15年后是否成年:{age +15 >= 18}')
