my_list = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
print(my_list)
# 去重
my_list = list(set(my_list))
print(my_list)

if 111 in my_list:
    print("111在列表中")
else:
    print("111不在列表中")
