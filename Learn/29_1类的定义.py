# 1.定义类
class Cat:
    def eat(self):
        print("小猫爱吃鱼...")
    def drink(self):
        print("小猫爱喝水...")

# 2.创建对象-可创建多个对象来调用这个类
tom = Cat()
Jack = Cat()

# 3.通过对象调用方法
print('由tom调用:')
tom.eat()
tom.drink()
print('由Jack调用:')
Jack.eat()
Jack.drink()
