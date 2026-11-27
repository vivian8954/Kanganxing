my_dict = {'name':'zhang san', 'age':18, 'sex':'man', 'hobby':['playing', 'reading']}
print('遍历字典的键：')
print(my_dict.keys())
for key in my_dict:
    print(key)

print('\n遍历字典的值：')
print(my_dict.values())
for value in my_dict.values():
    print(value)

# 遍历键值对
print('\n遍历字典的键值对：')
print(my_dict.items())
for key, value in my_dict.items():
    print(key, ':', value)
