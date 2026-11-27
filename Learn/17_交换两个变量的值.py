"""
交换两个变量的值
"""
# 方式一 临时变量法
a = 10
b = 20
c = 1000
print('交换前：a =', a, 'b =', b, 'c =', c)
a, b, c = b, c, a
print('交换后：a =', a, 'b =', b, 'c =', c)

# 方式二
x, y, z, q = [1, 2, 3, 4]
print('x =', x, 'y =', y, 'z =', z, 'q =', q)
x, y, z, q = y, z, q, x
print('x =', x, 'y =', y, 'z =', z, 'q =', q)
