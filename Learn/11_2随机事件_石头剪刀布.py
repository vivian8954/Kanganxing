import random
"""
1.从控制台输入要出的拳一石头（1）/剪刀（2）/布（3）
2.电脑随机出拳一先假定电脑只会出石头，完成整体代码功能
3.比较胜负
"""


player = int(input('请输入【1】石头 【2】剪刀【3】布 对应的数值：'))
print(f'您出的是：{player}')
computer = random.randint(1, 3)  # 1-3之间的随机整数
print(f'电脑出的是：{computer}')
# 3.比较胜负
# 玩家胜利
# 玩家出石头，电脑出剪刀 or 玩家出剪刀，电脑出布 or 玩家出布，电脑出石头
if (player == 1 and computer == 2) or \
        (player == 2 and computer == 3) or \
        (player == 3 and computer == 1):
    print('您胜利啦！')
    # 平局
elif player == computer:
    print('平局。')
    # 电脑胜利
else:
    print('电脑胜利！')
