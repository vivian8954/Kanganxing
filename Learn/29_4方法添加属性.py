class Cat:
    def __init__(self, name):
        print("我是__init__，初始化方法被调用了")
        self.name = name
    def eat(self):
        print(f"{self.name}小猫爱吃鱼...")
    def drink(self):
        print(f"{self.name}小猫爱喝水...")

# 创建对象，类名()
tom = Cat("Tom")
print(tom.name)
tom.eat()

blue_cat = Cat("Blue")
print(blue_cat.name)
blue_cat.drink()