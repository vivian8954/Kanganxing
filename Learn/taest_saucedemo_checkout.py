# -*- coding: utf-8 -*-
"""
SauceDemo 端到端测试：登录 -> 添加两款商品到购物车 -> 填写信息并结算

默认以有头模式（可见浏览器窗口）运行。

安装依赖：
    pip install pytest playwright
    # 若本机无 Edge/Chrome，需下载内核：playwright install chromium

运行：
    pytest test_saucedemo_checkout.py -v -s
    # 无头模式：HEADED=0 pytest test_saucedemo_checkout.py -v
    # 指定内核：BROWSER_CHANNEL=chrome pytest test_saucedemo_checkout.py -v
"""
import os

import pytest
from playwright.sync_api import Page, expect, sync_playwright

BASE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

PRODUCTS = [
    ("sauce-labs-backpack", "Sauce Labs Backpack"),
    ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
]

# 默认有头；默认优先使用系统 Edge（Windows 常见），可用环境变量覆盖
HEADED = os.getenv("HEADED", "1") != "0"
BROWSER_CHANNEL = os.getenv("BROWSER_CHANNEL", "msedge").strip()


@pytest.fixture(scope="function")
def browser_page():
    """每个用例独立启动一个可见浏览器窗口。"""
    with sync_playwright() as p:
        launch_kwargs = {"headless": not HEADED}
        browser = None
        if BROWSER_CHANNEL:
            try:
                browser = p.chromium.launch(channel=BROWSER_CHANNEL, **launch_kwargs)
            except Exception as exc:  # 系统无该内核时回退到 Playwright 内置 chromium
                print(f"[warn] channel={BROWSER_CHANNEL} 启动失败，回退内置内核: {exc}")
        if browser is None:
            browser = p.chromium.launch(**launch_kwargs)

        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


@pytest.fixture(scope="function")
def logged_in_page(browser_page: Page) -> Page:
    """前置：打开首页并以 standard_user 登录。"""
    browser_page.goto(BASE_URL, wait_until="domcontentloaded")
    expect(browser_page.locator("#user-name")).to_be_visible()
    browser_page.locator("#user-name").fill(USERNAME)
    browser_page.locator("#password").fill(PASSWORD)
    browser_page.locator("#login-button").click()
    expect(browser_page).to_have_url(f"{BASE_URL}inventory.html")
    expect(browser_page.locator(".title")).to_have_text("Products")
    return browser_page


def _add_two_products(page: Page) -> None:
    """把 PRODUCTS 中的两款商品加入购物车，并断言角标数量为 2。"""
    for sku, _name in PRODUCTS:
        page.locator(f"#add-to-cart-{sku}").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text(str(len(PRODUCTS)))


def test_login(logged_in_page: Page) -> None:
    """验证登录成功并进入商品列表页。"""
    expect(logged_in_page.locator(".inventory_item")).to_have_count(6)


def test_add_two_products_to_cart(logged_in_page: Page) -> None:
    """验证两款商品已加入购物车。"""
    _add_two_products(logged_in_page)
    logged_in_page.locator(".shopping_cart_link").click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}cart.html")
    expect(logged_in_page.locator(".cart_item")).to_have_count(len(PRODUCTS))
    for _sku, name in PRODUCTS:
        expect(logged_in_page.locator(".inventory_item_name", has_text=name)).to_be_visible()


def test_checkout(logged_in_page: Page) -> None:
    """完整流程：加购两款商品 -> 购物车 -> 填写收货信息 -> 完成结算。"""
    _add_two_products(logged_in_page)

    logged_in_page.locator(".shopping_cart_link").click()
    logged_in_page.locator("#checkout").click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}checkout-step-one.html")

    logged_in_page.locator("#first-name").fill("Test")
    logged_in_page.locator("#last-name").fill("User")
    logged_in_page.locator("#postal-code").fill("100001")
    logged_in_page.locator("#continue").click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}checkout-step-two.html")
    expect(logged_in_page.locator(".cart_item")).to_have_count(len(PRODUCTS))

    logged_in_page.locator("#finish").click()
    expect(logged_in_page).to_have_url(f"{BASE_URL}checkout-complete.html")
    expect(logged_in_page.locator(".complete-header")).to_have_text("Thank you for your order!")
    logged_in_page.screenshot(path="saucedemo_checkout_complete.png", full_page=True)
