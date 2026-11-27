"""
1．房子(House）有户型、总面积和家具名称列表－新房子没有任何的家具
2.家具(HouseItem）有名字和占地面积，其中
-席梦思(bed）占地 4平米
-衣柜(chest)占地2平米
- 餐桌(table）占地1.5平米
3．将以上三件家具添加到房子中
4．打印房子时，要求输出：户型、总面积、剩余面积、家具名称列表
剩余面积：
1.在创建房子对象时，定义一个剩余面积的属性，初始值和总面积相等
2.当调用add_item方法，向房间添加家具时，让剩余面积-=家具面积
"""
import time


class House:
    def __init__(self, house_type, total_area):
        self.house_type = house_type
        self.total_area = total_area
        self.free_area = total_area # 剩余面积
        self.furniture = [] # 家具列表
        self.furniture_area = [] # 家具面积列表
    def __str__(self):
        return f"房子的户型是{self.house_type}，总面积是{self.total_area}，剩余面积是{self.free_area}，\n家具列表是{self.furniture}，\n面积列表是{self.furniture_area}"
    def add_item(self, item):
        self.furniture.append(item.name)
        self.furniture_area.append(item.area)
        self.free_area -= item.area

class HouseItem:
    def __init__(self, name, area):
        self.name = name
        self.area = area
    def __str__(self):
        return f"置办家具：{self.name}，占地：{self.area}平米"


my_house = House("两室一厅", 100)
print(my_house)
time.sleep(3)
bed = HouseItem("席梦思", 4)
print(bed)
my_house.add_item(bed)
print(my_house)
time.sleep(2)
chest = HouseItem("衣柜", 2)
print(chest)
my_house.add_item(chest)
print(my_house)
time.sleep(2)
table = HouseItem("餐桌", 1.5)
print(table)
my_house.add_item(table)
print(my_house)
