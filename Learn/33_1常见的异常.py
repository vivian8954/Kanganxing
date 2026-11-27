try:
    num = input("请输入一个数字：")
    num = int(num)
    # 数据转换正确时，输出数据内容
    print(num)
    # 数据转换错误时，提示输入正确数据
except:
    print("输入的不是数字")
