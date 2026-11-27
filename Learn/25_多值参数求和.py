# *args元组求和
def my_sum(*args):
    num = 0
    for i in args:
        num += i
    print(num)

my_sum(1, 2, 3)
my_sum(1, 2, 3, 4, 5)
my_sum()

# 使用my_sum函数对列表和元组中的数据进行求和
my_list = [1, 2, 3]
my_tuple = (4, 5, 6)
my_sum(*my_list)
my_sum(*my_tuple)
my_sum(my_list[0], my_list[1], my_list[2])
my_sum(my_tuple[0], my_tuple[1], my_tuple[2])
