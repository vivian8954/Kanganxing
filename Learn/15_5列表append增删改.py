my_list = ['vivian',18,'2013/02/11',False]
print(my_list)
# 添加数据append
my_list.append('172.3')
print(my_list)
my_list.append('柏杨')
print(my_list)

# 删除数据pop
result = my_list.pop(1)
print('删除的数据为：',result)
print(my_list)

# 修改数据
my_list[0] = 'Monkey'
print(my_list)