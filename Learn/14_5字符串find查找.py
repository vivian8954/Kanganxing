my_str = 'bhydhcdbhellojcdscjlkvivian'
print(my_str.find('hello'))
print(my_str.find('p'))
name = input('请输入要判断的数据：')
result = my_str.find(name)
if result == -1:
    print('你所输入的字符串不存在')
else:
    print(f'{name}所在的位置为第{result}个')