import pytest

from Learn.tools import add

data_list = [(1,10,10),(1,5,6),(9,7,16)]
class TestAdd:
    # 参数化
    @pytest.mark.parametrize("a,b,expect",data_list)
    def test_add_1(self,a,b, expect):
        print(f'加法：{a},{b},预期结果为：{expect}')
        #断言
        assert expect == add(a, b)


    # def test_add_2(self):
    #     print('1,5,6')
    #     assert 6 == add(1, 5)
    #
    # def test_add_3(self):
    #     print('9,7,16')
    #     assert 16 == add(9, 7)
