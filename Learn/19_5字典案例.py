data = [
    {'desc': '用户名为空', 'username': '', 'password': '123456', 'code': '8888', 'expected': '用户名不能为空'},
{'desc': '用户名为空', 'username': 'super', 'password': '1256265', 'code': '8888', 'expected': '密码错误'},
{'desc': '用户名为空', 'username': 'super', 'password': '123456', 'code': 'ded', 'expected': '验证码错误'}
]
# 1.按照如下格式打印输出内容
# 用户名：xxx 密码：xxx 验证码：xxx 预期结果：xxx
for item in data:
    print(f'用户名：{item.get("username")} 密码：{item.get("password")} 验证码：{item.get("code")} 预期结果：{item.get("expected")}')

# 2.将测试数据组成[(),()]--->后续自动化测试中需要的数据类型
new_list = []
for item in data:
    new_list.append((item.get("username"), item.get("password"), item.get("code"), item.get("expected")))
print(new_list)
