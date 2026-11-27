class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):  # 当print打印对象时，会自动调用这个方法
        return f"狗狗：{self.name}, 年龄：{self.age}岁"

    def bark(self):
        print(f"狗狗{self.name}, {self.age}岁，汪汪叫...")



dog = Dog("旺财", 2)
print(dog.name, dog.age)
print(dog)

dog.bark()

