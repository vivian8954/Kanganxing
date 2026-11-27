"""
1.定义一个模块tools.py，定义函数实现对两个数据进行加法操作的函数add_2num，并返回相
加之和的结果；再定义一个实现对三个数据进行加法操作的函数add_3_num，并返回相加之和的
结果；最后新定义一个代码文件，对这两个函数进行测试调用，并在控制台打印结果
"""
from tools import sum_2_num, add_3_num
import random

"""
1．定义一个函数，make_data，在列表中随机创建10个1-100之间的数字
2．定义一个函数，my_max，返回列表中最大的数字
"""
def make_data():
    data = []
    for i in range(10):
        data.append(random.randint(1, 100))
    print(data)
    return data

def my_max(data):
    max_num = data[0]
    for i in data:
        if i > max_num:
            max_num = i
    return max_num

def my_min(data):
    min_num = data[0]
    for i in data:
        if i < min_num:
            min_num = i
    return min_num

"""
定义一个函数sum，计算1+2+3+...+n的值，并打印结果
"""
def sum(n):
    result = 0
    for i in range(1, n + 1):
        result += i
    return result

def input_num():
    num = int(input('请输入一个数字：'))
    print('你输入的数字是：', num)
    return num


"""
有如下列表：
my_list =[{'id': 1,'money': 10},{'id': 2,'money': 20},{'id': 3,'money': 30},{'id':4,'money': 40}]
要求：定义一个函数func，功能如下
1．如果字典中ID的值为奇数，则对money的值加20
2．如果字典中ID的值为偶数，则对money的值加10
3．打印输出列表，查看最终的结果
"""

def func(my_list):
    for i in my_list:
        if i['id'] % 2 == 1:
            i['money'] += 20
        else:
            i['money'] += 10
    print(my_list)



"""
定义一个函数，作用：打印每个字符出现的次数.
要求：1．在函数内部提示输入一个字符串
2．输出每个字符出现的次数
3．相同的字符，只打印一次
"""
def char_count():
    my_str = input('请输入一个字符串：')
    my_dict = {}
    for i in my_str:
        my_dict[i] = my_str.count(i)
    print(my_dict)
# char_count()

"""
设计过7游戏，定义一个函数func，要求如下
1．该函数接收一个参数，为一个1-99之间的数字
2．函数对该数字到99之间的所有数字进行判断，如果数字包含7或者是7的倍数，
则输出“过...”，否则输出具体的数字，直到输出“过...”，结束游戏
"""
def func():

    number = int(input('请输入一个数字：'))

    for i in range(number, 100):
        if '7' in str(i) or i % 7 == 0:
            print('过...', i)
            break
        else:
            print(i)




if __name__ == '__main__':
    # print(sum_2_num(10, 20))
    # print(add_3_num(10, 20, 30))
    # print('10个随机数是：', make_data())
    # print('最大值是：', my_max(make_data()))
    # print('最小值是：', my_min(make_data()))
    # print('1+2+3+...+n的和是：', sum(input_num()))
    # my_list = [
    #     {'id': 1, 'money': 10},
    #     {'id': 2, 'money': 20},
    #     {'id': 3, 'money': 30},
    #     {'id': 4, 'money': 40}]
    # print(my_list)
    # func(my_list)
    # char_count()
    func()
