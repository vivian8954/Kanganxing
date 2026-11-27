# name = input('请输入用户名：')
# psd = input('请输入密码')
# if name == 'super' and psd == 'abcd1234':
#     print('登录成功')
# else:
#     print('账号名或者密码不正确')
"""
1.定义两个整数变量python_score、c_score，使用input获取成绩编写代码判断成绩
2.要求只要有一门成绩>60分就输出合格
"""
# python_score = int(input('请输入python考试成绩：'))
# c_score = int(input('请输入c语言考试成绩：'))
# if python_score > 60 or c_score > 60:
#     print(f'python {python_score}分，c语言 {c_score}分，本次考试合格')
# else:
#     print(f'python {python_score}分，c语言 {c_score}分，两门都不及格，本次考试不合格')

"""
1.定义score变量记录考试分数
2.如果分数是大于等于90分显示优
3.如果分数是大于等于80分并且小于90分显示良
4.如果分数是大于等于70分并且小于80分显示中
5.如果分数是大于等于60分并且小于70分显示差
6.其它分数显示不及格
"""
score = float(input('请输入python考试成绩：'))
if (score >= 80) and score <= 100:
    print(f'成绩 {score}分，本次考试【优】')
elif (score >= 80) and score < 90:
    print(f'成绩 {score}分，本次考试【良】')
elif (score >= 70) and score < 80:
    print(f'成绩 {score}分，本次考试【中】')
elif (score >= 60) and score < 70:
    print(f'成绩 {score}分，本次考试【差】')
elif (score >= 0) and score < 60:
    print(f'成绩 {score}分，本次考试【不及格】')
else:
    print(f'成绩 {int(score)}分，【分数无效】')
