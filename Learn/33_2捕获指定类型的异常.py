# try:
#     num = input("请输入一个数字：")
#     num = int(num)
#     # 数据转换正确时，输出数据内容
#     a = 10/num
#     print(num)
#     # 数据转换错误时，提示输入正确数据
# except ZeroDivisionError:
#     print("除零错误")
# except ValueError:
#     print("输入的不是数字")


try:
    num = input("请输入一个数字：")
    num = int(num)
    # 数据转换正确时，输出数据内容
    a = 10/num
    print(num)
    # 数据转换错误时，提示输入正确数据
except Exception as e:
    print("发生了异常：\n", e)
