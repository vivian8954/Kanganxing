# # 1.打开文件
# # 2.写入文件
# with open("C:\\Users\\yungs\\Desktop\\学习材料.txt", "w") as f:
#     # 写入文件,会覆盖原内容
#     f.write("hello world")

# # 3.追加内容
# with open("C:\\Users\\yungs\\Desktop\\学习材料.txt", "a") as f:
#     f.write("\nhello world\n")
#
# # 4.读取全部文件内容
# with open("C:\\Users\\yungs\\Desktop\\学习材料.txt", "r") as f:
#     content = f.read()
#     print(content)


# # 5.读取文件行
with open("C:\\Users\\yungs\\Desktop\\学习材料.txt", "r") as f:
    while True:
        lines = f.readlines()
        # 判断是否到达文件末尾
        if not lines:
            break
        print(lines,end='')

# # 6.遍历文件行
# with open("C:\\Users\\yungs\\Desktop\\学习材料.txt", "r") as f:
#     for line in f:
#         print(line)

# # 关闭文件
# f.close()  # 文件在with语句块自动关闭，这里 redundant
