# 针对某网站的登录功能进行测试，现在需要将测试数据定义为json文件，以便于在自动化测试中使用，每一组测试数据应该
# 包含如下信息：
# 用户名 密码 验证码 预期结果 测试描述（标题)
# desc password expect username
import json

def build_data():
    with open('user_login.json') as f:
        data = json.load(f)
    new_list = []
    for i in data:
        # i.pop('desc')
        new_list.append([i['username'], i['password'], i['code'], i['expect'], i['desc']])
    return new_list
if __name__ == '__main__':
    print(build_data())

