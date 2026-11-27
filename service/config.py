# config.py
from pathlib import Path

DEFAULT_OUT_DIR = Path(r"F:\Script")
DEFAULT_BROWSER_JS = Path(
    r"C:\Users\yungs\PycharmProjects\Production\KanganXing\JS\browser.js"
)
BASE_URL = "https://www.saucedemo.com/"
DEFAULT_USER = "standard_user"
DEFAULT_PASSWORD = "secret_sauce"

DEFAULT_FIRST_NAME = "Test"
DEFAULT_LAST_NAME = "User"
DEFAULT_POSTAL_CODE = "100001"

PRODUCTS = [
    {"sku": "sauce-labs-backpack", "name": "Sauce Labs Backpack"},
    {"sku": "sauce-labs-bolt-t-shirt", "name": "Sauce Labs Bolt T-Shirt"},
]

PHASES = [
    ("p1", "访问站点首页", "01_login.png"),
    ("p2", "登录 standard_user", "02_inventory.png"),
    ("p3", "添加两款商品", "03_cart_badge.png"),
    ("p4", "进入购物车核对", "04_cart.png"),
    ("p5", "填写收货信息 / 订单概览", "05_overview.png"),
    ("p6", "完成结算", "06_complete.png"),
]

DEFAULT_VIEWPORT = {"width": 1440, "height": 900}
DEFAULT_WAIT = 350
