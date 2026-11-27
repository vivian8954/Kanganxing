"""
#字符串的基本使用
"""
# #定义一个字符串str1，字符串的内容为"helloworldanditcastanditheimaandPython"
# str1 = "hello world and it cast and it hei ma and Python"
#
# #在字符串stri中查找字符串and的下标
# index_and = str1.find("and")
# print("and对应的下标是：", index_and)
#
# #在字符串str1中查找字符串good'的下标
# index_good = str1.find("good")
# print("good对应的下标是：", index_good)
#
# #将字符串str1中的and替换为or
# print("替换前的字符串是：", str1)
# str2 = str1.replace("and", "or")
# print("替换后的字符串是：", str2)
#
# #将字符串str1按照空白字符进行切割，保存到变量1ist1中
# list1 = str1.split()
# print("切割后的列表是：", list1)
#
# #使用_*_将1ist1中的字符串进行连接
# list2 = '_*_'.join(list1)
# print("连接后的字符串是：", list2)
#
# #使用逗号将1ist1中的字符串进行连接
# list3 = ', '.join(list1)
# print("连接后的字符串是：", list3)


"""
#2.列表的基本使用
"""
# # 2.练习对列表的增删改查统计的操作，具体操作如下:
# # 1)声明一个列表，创含的数据有：["hello"，"python"，"it cast"，"hel1o"]
# list1 = ['hello', 'python', 'it cast', 'hello']
# print("原始列表是：", list1)
#
# # 2)在列表中追加一个数据："heima"
# list1.append("heima")
# print("追加\"heima\"后的列表是：", list1)
#
# # 3）删除列表中的第二个数据
# list1.pop(1)
# print("删除第二个数据后的列表是：", list1)
#
# # 4)删除列表中的数据："heima"
# list1.remove("heima")
# print("删除\"heima\"后的列表是：", list1)
#
# # 5)将列表中的第二个数据改为："chuanzhi"
# list1[1] = "chuanzhi"
# print("将第二个数据改为\"chuanzhi\"后的列表是：", list1)
#
# # 6)在控制台打印列表中的第一个元素
# print("列表中的第一个元素是：", list1[0])
#
# # 7)统计列表中"hel1o"字符串出现的次数
# count = list1.count("hello")
# print("列表中\"hello\"字符串出现的次数是：", count)
#
# # 8）在控制台打印列表的长度
# print("列表的长度是：", len(list1))
#
# # 9）循环遍历列表中的所有数据
# for item in list1:
#     print("数据是：", item)
#
# # 10）循环遍历列表中的所有数据,且加上序号
# for index, item in enumerate(list1):
#     print("第", index + 1, "个数据：", item)

"""
3.列表操作
有一个列表，判断列表中的每一个元素是否以s或e结尾，如果是，则将其放入一个新的列表中，最后输出这个新的列表
"""
# # 写法一：
# # 有一个列表，判断列表中的每一个元素是否以s或e结尾，如果是，则将其放入一个新的列表中，最后输出这个新的列表
# list1 =["red", "apples", "orange", "pink", "bananas", "blue", "black", "white"]
# for item1 in list1:
#     print("数据是：", item1)
# new_list = [
#     item for item in list1
#     if item.endswith("s") or item.endswith("e")]
# print("新的列表是：", new_list)

# # 写法二：
# my_list =["red", "apples", "orange", "pink", "bananas", "blue", "black", "white"]
# print("原始列表是：", my_list)
#
# new_list = []
# for i in my_list:
#     if i[-1] == "s" or i[-1] == "e":
#         new_list.append(i)
# print("新的列表是：", new_list)


"""
4.随机抽签
"""
# # 方法1
# import random
# m = 0
# while True:
#     print("第", m + 1, "次抽签↓↓↓↓↓")
#     m += 1
#     name_list = []
#     for i in range(5):
#         name = input("请输入学生的名字：")
#         name_list.append(name)
#     num = random.randint(0, 4)
#     print("随机获取的一个学生的名字是：", name_list[num])



# # 方法2
# import random
# # 1. 使用input输入5个学生的名字存入列表
# while True: # 这里改成无限循环
#     names = input("请输入5个学生的名字，用逗号隔开：")
#     name_list = names.split(",")
#     # 2．随机的获取2个学生的名字并打印
#     print("随机获取的一个学生的名字是：", random.choice(name_list))
#     print("随机获取的2个学生的名字是：", random.sample(name_list, 2))



"""
5.已有列表nums=[10, 20, 30, 40, 50]的基础上加10，打印列表
"""
# nums = [10, 20, 30, 40, 50]
# print("原始列表是：", nums)
# new_nums = [num + 10 for num in nums]
# print("新的列表是：", new_nums)
