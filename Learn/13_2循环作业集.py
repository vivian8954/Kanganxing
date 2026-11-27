"""
判断是否为闰年
"""
# year = int(input("请输入年份："))
# if year % 4 == 0:
#     print(f"{year}年是闰年")
# else:
#     print(f"{year}年不是闰年")


"""
求1-100内偶数的和
"""
# num = 0
# for i in range(101):
#     if i % 2 == 0:
#         num += i
#         print(num, end='--->')
#         print(i)
# print('总和为：', num)


"""
设计简易计算器，可以进行基本的加减乘除运算
"""
# input_number1 = float(input("请输入第一个数字："))
# input_number2 = float(input("请输入第二个数字："))
# input_operator = input("请输入运算符：")
# if input_operator == '+':
#     print(f'{input_number1} + {input_number2}={input_number1 + input_number2}')
# elif input_operator == '-':
#     print(f'{input_number1} - {input_number2}={input_number1 - input_number2}')
# elif input_operator == '*':
#     print(f'{input_number1} * {input_number2}={input_number1 * input_number2}')
# elif input_operator == '/':
#     print(f'{input_number1} / {input_number2}={input_number1 / input_number2}')
# else:
#     print("输入的运算符有误！")

"""

猜数字游戏：
1.电脑产生一个（1-100）的随机数，用户进行猜测（通过input输入)，直到猜中为止。
2.如果猜对了，输出：恭喜你猜对了，数字是xX。
3.如果猜的数字比随机数大，输出：猜测的数字太大了，继续加油
4.如果猜测的数字比随机数小，输出：猜测的数字有点小，再来一次
"""
import random
random_number = random.randint(1, 100)
print(f'随机数是{random_number}')
while True:
    input_number = int(input("请输入一个1-100的数字："))
    if input_number > 100 or input_number <= 0:
        print('----->请输入1-100内的有效数字。')
    else:
        if input_number == random_number:
            print(f"恭喜你猜对了，数字是{random_number}")
            break
        elif input_number > random_number:
            print("猜测的数字太大了，继续加油")
        else:
            print("猜测的数字有点小，再来一次")
print("游戏结束")


"""
需求：
1.提示用户输入登录系统的用户名和密码
2.校验用户名和密码是否正确(正确的用户名:admin、密码:123456)
3.如果用户名和密码都正确，打印“登录成功！”，并结束程序
4.如果用户名或密码错误，打印“用户名或密码错误！”，提示用户继续输入用户名和密码登录
5.如果用户输入的用户名为“exit”,则退出程序
"""
# while True:
#     input_username = input("请输入用户名：")
#     if input_username == "exit":
#         print("退出程序！")
#         break
#     input_password = input("请输入密码：")
#     if input_username == "admin" and input_password == "123456":
#         print("登录成功！")
#         break
#     else:
#         print("用户名或密码错误！请继续输入用户名和密码登录")