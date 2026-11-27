#定义一个tools类
class Tools:
    #在类的内部，方法的外部直接定义的变量，称为类属性
    count = 0
    tools_list = []
    def __init__(self, name):
        self.name = name
        #每创建一个对象，类属性加1
        Tools.count += 1
        Tools.tools_list.append(self.name)
        #打印tools_list内容
        print(Tools.tools_list)
        print('当前创建工具对象个数为：',Tools.count)

    #定义一个类方法
    @classmethod
    def show_count(cls):
        print('当前创建工具对象个数为：', cls.count)

    #定义一个静态方法
    @staticmethod
    def show_info():
        print('这是一个工具类')

#创建对象
print('当前创建工具对象个数为：', Tools.count)  # 输出：当前创建工具对象个数为： 0
Tools('扳手')
Tools('锤子')
Tools('锯子')
#调用类方法
Tools.show_count()
#调用静态方法
Tools.show_info()



