# 1，获取用户输入的用户名信息
name = input('请输入用户名：')
# 2.如果用户名信息是admin，就在控制台输出“欢迎admin登录"
if name == 'admin':
    print('欢迎admin登录。')
elif name == 'super':
    print('哟，超级管理员super来啦~')
else:
    print(f'{name}，欢迎你。')
