import json

with open("user.json", "r") as f:
    # 加载json数据
    result = json.load(f)
    for i in result:
        isStudent = "是" if i["isStudent"] == True else "否"
        print(" 姓名", i["name"], " 年龄", i["age"], " 是否为学生", isStudent, " 地址", i["address"])
