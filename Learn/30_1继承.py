class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"名字是{self.name}，年龄是{self.age}"
    def eat(self, food):
        print(f"{self.name}在吃【{food}】...")
    def sleep(self):
        print(f"{self.name}在睡觉")

class Cat(Animal):
    def catch(self, thing):
        print(f"【{self.age}】岁的【{self.name}】在抓【{thing}】...")

ani = Animal("小猫", 2)
print(ani)
ani.eat("鱼")
cat = Cat("小狸猫", '')
cat.catch("小耗子")
ani.sleep()
