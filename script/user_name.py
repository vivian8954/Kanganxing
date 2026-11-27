import time
def hello():
    print("hello world")
    print("已经推送了吗")

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"修改用户邮箱后重新push")
hello()
