# 1.使用单引号定义
my_str3 = 'hello'

# 2.使用双引号定义
my_str2 = "hello"

# 3.使用三引号定义
my_str3 = """hello"""
my_str4 = '''hello'''

# 4.
# 字符串本身包含单引号，定义的时候，不能使用单引号定义，用双引号
# 字符串本身包含双引号，定义的时候，不能使用双引号定义，用单引号
# I'm Jack
# Say "hello"
my_str5 = "I'm Jack"
my_str6 = 'Say "hello"'

# 5.使用转义字符 \'  --> '      \"  --> "
my_str7 = 'I\'m Jack'
print(my_str7)

# 原生字符串，在字符串前面加上r""，表示字符串的内容不会被转义
my_str8 = r'I\'m Jack'
print(my_str8)