# 读取json文件
import json

with open("user.json", "r") as f:
    # 加载json数据
    result = json.load(f)
    print("数据类型:", type(result))
    print("数据内容:\n", result)
    print(result[0]["name"])
    print(result[1]["hobbies"][0])
    print(result[1]["address"])