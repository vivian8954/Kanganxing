# 生成1-20之间数字的列表
my_list = list(range(1, 21, 3))
print('1-20之间步长为3的数字列表是：', my_list)
my_list1 = []
for i in range(1,10,2):
    my_list1.append(i)
print('1-10之间步长为2的数字列表是：', my_list1)

# 生成1-20之间偶数的列表
my_list2 = []
for i in range(1,21):
    if i % 2 == 0:
        my_list2.append(i)
print('1-20之间偶数的列表是：', my_list2)

# 生成1-20之间奇数的列表
my_list3 = []
for i in range(1,21):
    if i % 2 == 1:
        my_list3.append(i)
print('1-20之间奇数的列表是：', my_list3)
