my_str = 'abcncjcbn_cjk'
print(my_str)

# 取出abc数据
# 开始：0，结束3，步长1
print('取出abc数据:', my_str[0:3:1])
# 如果步长为1，可以不写
print('取出abc数据:', my_str[0:3])
# 如果步长>0，且开始位置为0 ，可以不写
print('取出abc数据:', my_str[:3])

# 取出cjk数据
print('取出cjk数据:', my_str[10:13:1])
print('取出cjk数据:', my_str[10:13])
print('取出cjk数据:', my_str[10:])

print('取出数据:', my_str[::])
print('取出数据:', my_str[::3])