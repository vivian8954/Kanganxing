# 1．获取用户输入的数字(input)
num = input("请输入一个数字：")
# 2.判断获取的数字是否整数
try:
    num = int(num)
    print(num, "是整数")
    if num % 2 == 0:
        print("是偶数")
    else:
        print("是奇数")
except Exception as e:
    print("输入错误,不是整数", e)
# 如果不是整数，提示输入错误
# 如果是整数，则进一步判断是奇数还是偶数
# 最终提示：程序运行结束
print("程序运行结束")
