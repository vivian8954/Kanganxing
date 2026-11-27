import os
from datetime import datetime
import pytest

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.dirname(__file__)
# 1. 自动创建reports文件夹，不存在就新建
report_dir = "reports"
if not os.path.exists(report_dir):
    os.makedirs(report_dir)

time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
report_name = f"report_{time_str}.html"

if __name__ == '__main__':
    print(BASE_DIR)
    pytest.main([
        "Learn",
        "script",
        "-v",
        "-s",#-s去掉，则会在报告中看错误
        "--full_report", report_name,
        "--title", "康安星自动化测试报告",
        "--tester", "测试工程师",
        "--desc", "单元测试执行结果"
    ])