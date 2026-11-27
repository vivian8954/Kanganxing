my_dict = {'name':'zhang san', 'age':18, 'sex':'man', 'hobby':['playing', 'reading']}

# 获取age(键存在）
print(my_dict['age'])
print(my_dict.get('age'))

# 获取weight(键不存在）
# print(my_dict['weight']) #--会报错
print(my_dict.get('weight'))#--不会报错，返回None。优先使用这种

#获取hobby列表中的第一个数据
print(my_dict['hobby'][0])
print(my_dict.get('hobby')[0])
print(my_dict.get('hobby'))