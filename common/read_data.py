import json
from config import BASE_DIR
def build_data():
    #绝对路径
    # with open('C:/Users/yungs/PycharmProjects/Production/KanganXing/test_data/add.json') as f:
    # 相对路径
    with open(BASE_DIR + '/test_data/add.json') as f:
        data_list = json.load(f)
    return data_list

def build_login_data():
    """读取登录用例数据"""
    with open(BASE_DIR + '/test_data/login.json') as f:
        data_list = json.load(f)
    new_list = []
    for i in data_list:
        new_list.append([i.get('username'), i.get('password'), i.get('expected')])
    return new_list

if __name__ == '__main__':
    print(build_login_data())
