# 方式一 类实例化
# 1.1 空元组 没有实际意义
my_tuple = tuple()
print(my_tuple)
# 1.2   非空元组 字符串转换为元组
my_tuple1 = tuple('vivian')
print(my_tuple1)
# 1.2   非空元组 列表转换为元组
my_tuple2 = tuple([1, 2, 3, 4, 5])
print(my_tuple2)
print('my_tuple2[1]:', my_tuple2[1])
# 方式二 直接使用()
my_tuple3 = ('vivian', 18, 173.4, '2013/02/11', False)
print(my_tuple3)
print('my_tuple3[0]:', my_tuple3[0])
my_tuple5 = (['vivian', 18, 173.4, '2013/02/11', False],
             ['Lucy',17,153.5,'2014/07/09',True])
print(my_tuple5)
print('my_tuple5[1]:', my_tuple5[1])
# 特殊 定义只有一个数据的元组
my_tuple4 = ('vivian',)

print(my_tuple4)
