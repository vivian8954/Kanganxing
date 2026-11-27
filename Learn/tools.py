# 提供模块功能，设置密码长度最少8位，否则抛出异常
def set_password():
    password=input('请输入密码（长度最少8位）：')
    if len(password) >= 8:
        return password
    else:
        # 直接抛出异常
        raise Exception('密码长度最少8位')

def add(a, b):
    return a + b

def login(username, password):
    if username == 'admin' and password == '123456':
        return '登录成功'
    else:
        return '登录失败'
