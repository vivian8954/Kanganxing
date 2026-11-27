#定义狗类，具有名字和年龄属性
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"名字是{self.name}，年龄是{self.age}"

    def bark(self, voice):
        print(f"【{self.name}】在【{voice}】叫...")

class XTDog(Dog):
    def __init__(self,name, age, mp):
        # 继承了父类的name, age属性
        super().__init__(name, age) # 扩展式重写
        # 新增了mp属性-法力值
        self.mp = mp
    def bark(self, voice): # 覆盖式重写
        print(f"【{self.name}】修炼【{self.age}】年,法力值【{self.mp}】，在【{voice}】吼...")

dog = Dog("旺财", 2)
dog.bark("喵喵喵")
xt = XTDog("小黑", 100, 99.99)
# xt.berk("吼吼吼")
xt.bark("汪汪汪")

