import random
#1.使用随机数向列表添加10个1-20之间的随机数
my_list = []
for i in range(10):
    random_num = random.randint(1,20)
    # print(random_num)
    my_list.append(random_num)
print(my_list)
#2，统计数据8出现的个数
print('数据8在list中出现的次数',my_list.count(8))
#3．删除最后一个数据
my_list.pop()
print('删除最后一个数据后：',my_list)
#4.修改第一个数据为8
my_list[0] = 8
print('修改后：',my_list)
#5，再次统计数据8出现的个数
print('数据8在list中出现的次数',my_list.count(8))