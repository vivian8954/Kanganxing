#定义人类，姓名和年龄属性
class Person:
    def __init__(self, name, age):
        self.name = name
        #将年龄设置成私有
        self.__age = age
    def __str__(self):
        return f"名字是：{self.name}，年龄是：{self.__age}"

    #定义一个公有方法，修改私有属性
    def set_age(self, age):
        if 0 < age < 100:
            self.__age = age
        else:
            print(f"年龄设置{age}错误，请输入0-100的数字")

xw = Person("小王", 18)
print(xw)

# xw.__age =20 #此时修改的是一个新的属性，而不是原来的私有属性
xw.set_age(2000)
print(xw)
