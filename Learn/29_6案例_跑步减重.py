class Person:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return f"姓名：{self.name} ，当前体重：{self.weight}kg"

    def run(self):
        print(f"【{self.name}】 正在跑步...，体重减轻了0.5kg")
        self.weight -= 0.5
    def eat(self):
        print(f"【{self.name}】 正在吃东西...，体重增加了1kg")
        self.weight += 1

p = Person("小明", 72.2)
# print(p)
# p.run()
# print(p)
# p.eat()
# print(p)
# p.run()
# print(p)
