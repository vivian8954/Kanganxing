class Login:
    def __init__(self, username, password, code):
        self.username = username
        self.password = password
        self.code = code
    def __str__(self):
        return f"用户名：{self.username} ，密码：{self.password} ，验证码：{self.code}"
    def login(self):
        print(f"正在登录：{self.username} , {self.password} , {self.code}")
        while True:
            self.username = input("请输入用户名：")
            self.password = input("请输入密码：")
            self.code = input("请输入验证码：")
            if self.code == "8888":
                if self.username == "admin" and self.password == "123456":
                    print("登录成功!")
                    return
                else:
                    print("账号或密码错误，登录失败!")
            else:
                print("验证码错误!")

login = Login('', '', '') #初始化先给空值，在循环中由用户输入
login.login()
