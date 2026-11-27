age = int(input('请输入您的年龄'))
if age > 18:
    print(f'你现在{age}岁，已经成年')
elif age <= 0:
    print(f'你现在才{age}岁？输错了吧~')
    age += 18
    print(f'{age}年后再来网吧吧')
else:
    print(f'你现在才{age}岁，您还没有成年哦')
