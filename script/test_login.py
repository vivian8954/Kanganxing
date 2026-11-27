from Learn.tools import login
import pytest
from common.read_data import build_login_data

class TestLogin:
    """登录测试类"""
    # def setup_class(self):
    #     print("1.打开浏览器，开始登录测试")
    # def teardown_class(self):
    #     print("5.关闭浏览器登录测试结束")
    #
    # def setup(self):
    #     print("打开登录页面")
    #
    # def teardown(self):
    #     print("关闭登录页面")

    @pytest.mark.parametrize('username,password,expected', build_login_data())
    def test_username_password_ok(self, username, password, expected):
        print(f"\n正在测试：{username} , {password}，预期结果：{expected}")
        # 判断预期结果与实际结果是否相符
        assert login(username, password) == expected
