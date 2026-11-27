# 学生信息管理系统
# 需求：按照以下要求完成代码的编写
# 第一步：录入学生信息
# 1)提示用户在控制台输入3个学生的信息，学生信息包含姓名、年龄
# 2)要求：封装录入单个学生信息的函数，并返回学生的信息
# 第二步：展示学生列表信息
# 1)封装打印学生信息的函数，格式要求如右图：
# ----学生列表信息----
# 1     张三      19
# 2     李四      18
# 3     王五      22
# 第三步：统计学生总数
# 1)封装获取学生总数的函数，并对该函数进行调用和数据打印
# 第四步：查询学生信息
# 1)封装根据学生姓名查询学生信息的函数
# 2)提示用户“请输入要查询的学生姓名：”
# 3)如果存在，直接在控制台打印学生信息，格式为：“姓名：张三，年龄：25’
# 4)如果不存在，直接在控制台打印“对不起，名字叫【张三】的学生不存在
import time

# 定义一个列表，存储所有学生信息
# stu_list= [{"name": "张三", "age": 19}, {"name": "李四", "age": 18}, {"name": "王五", "age": 22}]
stu_list=[]
def input_student():
    """录入学生信息"""
    print("第一步：录入学生信息:")
    name = input("请输入学生姓名：")
    age = input("请输入学生年龄：")
    student_dict = {"name": name, "age": age}
    return student_dict

def show_info():
    """展示学生列表信息"""
    print("第二步：展示学生列表信息：\n----学生列表信息----")
    n = 1
    for i in stu_list:
        print(f"{n}     {i.get('name')}      {i.get('age')}")
        n += 1
    print("-" * 20)

def count_students():
    """统计学生总数"""
    print("第三步：统计学生总数")
    return len(stu_list)

def select_student():
    """查询学生信息"""
    while True:
        name = input("第四步：查询学生信息\n请输入要查询的学生姓名：")
        for i in stu_list:
            if i.get("name") == name:
                print(f"姓名：{i.get('name')}，年龄：{i.get('age')}")
                return
        print(f"对不起，名字叫【{name}】的学生不存在")



if __name__ == '__main__':
    # 循环录入3条学生信息，并存储在列表中
    for i in range(3):
        stu = input_student()
        stu_list.append(stu)
    print(stu_list) # 执行完一起打印学生信息
    time.sleep(3)  # 让程序暂停3秒
    show_info()
    time.sleep(3)  # 让程序暂停3秒
    num = count_students()
    print(f"学生总数：{num}")
    time.sleep(3)  # 让程序暂停3秒
    select_student()


