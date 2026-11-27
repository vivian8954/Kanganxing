my_dict = {'name':'zhangsan', 'age':18, 'sex':'man', 'hobby':['playing', 'reading']}
print('原字典：', my_dict)
# 将age改为20
my_dict['age'] = 20
print('年龄改为20：',my_dict)

# 添加体重
my_dict['weight'] = 70
print('添加体重：',my_dict)

# 删除sex
del my_dict['sex']
print('删除sex：',my_dict)

# 删除hobby中的reading
my_dict['hobby'].pop(0)
my_dict['hobby'].append('working')
my_dict['hobby'].append('sleeping')
my_dict['hobby'].remove('reading')
print('删除hobby中的reading：',my_dict)
