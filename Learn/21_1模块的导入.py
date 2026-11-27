import random
a = random.randint(1,10)
print(a)
from random import randint
b = randint(1,100)
print(b)
print(randint(1,10))

"""
1．定义一个模块tools.py，在模块中定义一个函数sum_2_num()，可以对两个数字求和
2.新定义一个代码文件，调用tools.py文件中的sum_2_num(）函数，对10和20求和
"""
from tools import sum_2_num
if __name__ == '__main__':
    print(sum_2_num(111.3, 112.3))
