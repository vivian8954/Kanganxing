from service.login_service import login
"""
1．模拟开发人员实现登录功能，定义一个函数能够接收用户输入（参数）的用户名、密码、验证
码，根据不同的测试数据返回不同的验证结果
2．已知正确的登录信息（用户名:admin、密码：123456、验证码：8888）
3.要求1:创建login_service.py模块开发登录功能代码，并存放到service包中
4.要求2:创建test_login.py模块开发测试代码，并存放到script包中
5．要求3:至少测试3种测试场景
"""
print(login('admin', '123456', '8888'))
print(login('admin', '123456', '999'))
print(login('admi', '123456', '8888'))
print(login('admin', '12346', '8888'))

