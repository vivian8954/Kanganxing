#在Dog类中封装game()方法
class Dog:
    def game(self):
        print(f"只是简单玩法")

class XTDog(Dog):
    def game(self):
        print(f"哮天犬需要在天上玩耍")
class AF(Dog):
    def game(self):
        print(f"阿尔法狗是机器狗")

class Person:
    def play_with_dog(self, d:Dog):
        print(f"人和狗在玩耍",end="->")
        d.game()

dog = Dog()
xtq = XTDog()
af = AF()
p =  Person()
p.play_with_dog(dog)
p.play_with_dog(af)
p.play_with_dog(xtq)


