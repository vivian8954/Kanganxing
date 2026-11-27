from unittest import result


def calc(a, b):
    return a + b, a - b, a * b, a / b

result = calc(10, 5)
print(result)

x, y, z, q = calc(10, 5)
print(x, y, z, q)
