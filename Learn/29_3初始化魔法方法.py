class Cat:
    def __init__(self):
        print("我是__init__，初始化方法被调用了")
        # self.name = None
Cat() # 会调用__init__方法
a = Cat() # 会调用__init__方法
b = Cat # 不会调用，只是把这个类的地址给了b
c = b() # 会调用__init__方法
e = c   # 不会调用，这不是创建对象

