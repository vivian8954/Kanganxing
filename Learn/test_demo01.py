# 书写测试类，类名以Test开头
import pytest


class TestDemo:
    # 书写测试方法，方法名以test开头
    def test_method_1(self):
        print("测试用例1")
    def test_method_2(self):
        print("测试用例2")

if __name__ == '__main__':
    # -v代表详细模式，-s代表运行时打印信息
    #执行时把用例里的print内容打印出来
    print("执行用例...")
    pytest.main(['-v', '-s', 'test_demo01.py'])
    # pytest.main(['-v', '-s', __file__])
