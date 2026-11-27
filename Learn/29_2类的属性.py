class Cat:
    def eat(self):
        print(f"{self.name}小猫爱吃鱼...")
    def drink(self):
        print(f"{self.name}小猫爱喝水...")

# 2.创建对象-可创建多个对象来调用这个类
tom = Cat()
Jack = Cat()

# 3.添加name属性
tom.name = "Tom"
tom.eat()
tom.drink()

Jack.name = "HHHH"
Jack.drink()
