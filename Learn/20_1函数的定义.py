def say_hello():
    """这是一个函数"""
    print('hello 1')
    print('hello 2')
    print('hello 3')
    print('hello 4')

def sum_2_nums():
    """这是sum_2_nums函数"""
    a = int(input('请输入第一个数字：'))
    b = int(input('请输入第二个数字：'))
    c = a+b
    print('求和的结果是', c)

def sum(a, b):
    """这是sum函数"""
    c = a+b
    print('求和的结果是', c)

def sum_3_nums(a, b, c):
    """这是sum_3_nums函数"""
    d = a+b/c
    print('计算的结果是', d)

# 需求：定义函数get_max返回两个数字中比较大的数字
def get_max(a, b):
    """这是get_max函数"""
    if a > b:
        return a
    elif a == b:
        print('两个数字相等')
        return b
    else:
        return b

"""
1. 定义名为 input_username 的函数, 获取用户输入的用户名
2. 定义名为 input_password 的函数,获取用户输入的密码
3. 定义名为 login 的函数,判断获取的用户名和密码信息
4. 要求当获取的用户名为:admin 并且密码为:123456 时,输出“登录成功!”，否则提示“用户名或
密码错误!沔
"""
def input_username():
    username = input('请输入用户名：')
    return username
def input_password():
    password = input('请输入密码：')
    return password
def login():
    while True:
        username = input_username()
        password = input_password()
        if username == 'admin' and password == '123456':
            print('登录成功!')
            break
        else:
            print('用户名或密码错误!')


if __name__ == '__main__':
    # say_hello()
    # sum_2_nums()
    # sum(10, 20)
    # sum(100, 20)
    # sum_3_nums(10, 20, 30)
    # result = get_max(10, 20)
    # print('较大的数字是', result+10)
    # print('较大的数字是', get_max(20, 20))
    login()
