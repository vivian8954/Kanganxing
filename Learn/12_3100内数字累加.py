# 初始数值
i = 0
# 定义变量，保存结果
num = 0
while i <= 100:
    num += i
    print(i, end=':')
    print(num)
    # 改变计数器
    i += 1
print('求和的结果为', num)
