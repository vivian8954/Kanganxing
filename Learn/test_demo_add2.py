import pytest
import json
from Learn.tools import add
from common.read_data import build_data

class TestAdd:
    # 参数化
    @pytest.mark.parametrize("a,b,expect",build_data())
    def test_add_1(self, a, b, expect):
        print(f'加法：{a},{b},预期结果为：{expect}')
        #断言
        assert expect == add(a, b)

