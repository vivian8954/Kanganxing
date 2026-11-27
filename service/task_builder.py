# task_builder.py
"""
提供单独构造每个阶段的 task 的函数，同时保留 shot 目录、progress 文件路径统一管理
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple
from config import BASE_URL, PRODUCTS, DEFAULT_VIEWPORT, DEFAULT_WAIT

def get_shot_path(shot_dir: Path, filename: str) -> str:
    return str(shot_dir / filename).replace("\\", "/")

def build_single_phase_task(
    phase_key: str,
    phase_name: str,
    shot_filename: str,
    shot_dir: Path,
    progress_path: Path,
    user: str,
    password: str,
    headless: bool,
    first_name: str,
    last_name: str,
    postal_code: str,
    prev_checkpoint: dict
) -> Tuple[Dict, List[Dict]]:
    """
    单独构造【单个阶段】的task steps
    返回 task dict + steps列表
    """
    steps: list[dict] = []
    def add(step_type: str, label: str, phase: str = "准备", **kwargs) -> None:
        item = {"type": step_type, "label": label, "phase": phase}
        item.update(kwargs)
        steps.append(item)

    def save() -> None:
        add("export", "保存检查点快照", "数据留存",
            path=str(progress_path).replace("\\", "/"), format="json")

    ids = json.dumps([p["sku"] for p in PRODUCTS], ensure_ascii=False)
    names = json.dumps([p["name"] for p in PRODUCTS], ensure_ascii=False)
    count = json.dumps(len(PRODUCTS))

    if phase_key == "p1":
        add("eval", "记录测试起始时间", js="({t: Date.now()})", var="t0")
        save()
        add("goto", "打开 SauceDemo 首页", phase_name, url=BASE_URL, waitUntil="domcontentloaded", timeout=45000)
        add("waitSelector", "等待登录表单渲染", phase_name, selector="#user-name", timeout=30000)
        add("screenshot", "登录页截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言登录页可用", phase_name, var="p1", js="""(() => {
            if (!document.querySelector('#user-name') || !document.querySelector('#login-button')) {
                throw new Error('登录表单元素缺失');
            }
            return {t: Date.now(), url: location.href, title: document.title};
        })()""")
        save()

    elif phase_key == "p2":
        add("fill", "填写用户名", phase_name, selector="#user-name", value=user)
        add("fill", "填写密码", phase_name, selector="#password", value=password)
        add("click", "点击登录按钮", phase_name, selector="#login-button")
        add("waitSelector", "等待商品列表出现", phase_name, selector=".inventory_list", timeout=30000)
        add("screenshot", "商品列表页截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言登录成功与商品数量", phase_name, var="p2", js="""(() => {
            const url = location.href;
            if (!url.includes('inventory.html')) throw new Error('登录后未进入商品列表: ' + url);
            const n = document.querySelectorAll('.inventory_item').length;
            if (n !== 6) throw new Error('商品数量异常，期望 6，实际 ' + n);
            return {t: Date.now(), url: url, title: document.title, productCount: n};
        })()""")
        save()

    elif phase_key == "p3":
        for product in PRODUCTS:
            add("click", f"添加 {product['name']}", phase_name, selector=f"#add-to-cart-{product['sku']}")
        add("screenshot", "加购后截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言购物车角标与商品", phase_name, var="p3", js="""(() => {
            const ids = __IDS__, names = __NAMES__;
            const badge = document.querySelector('.shopping_cart_badge');
            const badgeCount = badge ? Number(badge.textContent.trim()) : 0;
            if (badgeCount !== ids.length) throw new Error('购物车角标数量不符，期望 ' + ids.length + '，实际 ' + badgeCount);
            const picked = ids.map(function (id, i) {
                const btn = document.querySelector('#remove-' + id);
                if (!btn) throw new Error('商品未成功加入购物车: ' + names[i]);
                const card = btn.closest('.inventory_item');
                const priceEl = card ? card.querySelector('.inventory_item_price') : null;
                return {sku: id, name: names[i], price: priceEl ? priceEl.textContent.trim() : ''};
            });
            return {t: Date.now(), badgeCount: badgeCount, products: picked};
        })()""".replace("__IDS__", ids).replace("__NAMES__", names))
        save()

    elif phase_key == "p4":
        add("click", "进入购物车", phase_name, selector=".shopping_cart_link")
        add("waitSelector", "等待购物车条目渲染", phase_name, selector=".cart_item", timeout=30000)
        add("screenshot", "购物车页截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言购物车条目", phase_name, var="p4", js="""(() => {
            if (!location.href.includes('cart.html')) throw new Error('未进入购物车页: ' + location.href);
            const items = Array.from(document.querySelectorAll('.cart_item')).map(function (el) {
                const n = el.querySelector('.inventory_item_name'), p = el.querySelector('.inventory_item_price');
                return {name: n ? n.textContent.trim() : '', price: p ? p.textContent.trim() : ''};
            });
            if (items.length !== __COUNT__)
                throw new Error('购物车商品数量不符，期望 ' + __COUNT__ + '，实际 ' + items.length);
            return {t: Date.now(), url: location.href, itemCount: items.length, items: items};
        })()""".replace("__COUNT__", count))
        save()

    elif phase_key == "p5":
        add("click", "进入结算信息页", phase_name, selector="#checkout")
        add("waitSelector", "等待收货信息表单", phase_name, selector="#first-name", timeout=30000)
        add("fill", "填写 First Name", phase_name, selector="#first-name", value=first_name)
        add("fill", "填写 Last Name", phase_name, selector="#last-name", value=last_name)
        add("fill", "填写 Postal Code", phase_name, selector="#postal-code", value=postal_code)
        add("click", "提交收货信息", phase_name, selector="#continue")
        add("waitSelector", "等待订单概览", phase_name, selector=".summary_info", timeout=30000)
        add("screenshot", "订单概览页截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言订单概览与金额", phase_name, var="p5", js="""(() => {
            if (!location.href.includes('checkout-step-two.html'))
                throw new Error('未进入订单概览页: ' + location.href);
            const txt = function (s) { const e = document.querySelector(s); return e ? e.textContent.trim() : ''; };
            const items = Array.from(document.querySelectorAll('.cart_item .inventory_item_name'))
                .map(function (e) { return e.textContent.trim(); });
            if (items.length !== __COUNT__)
                throw new Error('订单概览商品数量不符，期望 ' + __COUNT__ + '，实际 ' + items.length);
            return {t: Date.now(), url: location.href, items: items,
                    subtotal: txt('.summary_subtotal_label'), tax: txt('.summary_tax_label'),
                    total: txt('.summary_total_label')};
        })()""".replace("__COUNT__", count))
        save()

    elif phase_key == "p6":
        add("click", "点击 Finish 完成结算", phase_name, selector="#finish")
        add("waitSelector", "等待结算成功页", phase_name, selector=".complete-header", timeout=30000)
        add("screenshot", "结算成功页截图", phase_name, path=get_shot_path(shot_dir, shot_filename), full=True)
        add("eval", "断言结算成功文案", phase_name, var="p6", js="""(() => {
            if (!location.href.includes('checkout-complete.html'))
                throw new Error('未进入结算完成页: ' + location.href);
            const h = document.querySelector('.complete-header');
            const header = h ? h.textContent.trim() : '';
            if (header !== 'Thank you for your order!') throw new Error('成功文案异常: ' + header);
            const d = document.querySelector('.complete-text');
            return {t: Date.now(), url: location.href, header: header,
                    text: d ? d.textContent.trim() : ''};
        })()""")
        save()

    task = {
        "url": BASE_URL,
        "headless": headless,
        "engine": "chromium",
        "viewport": DEFAULT_VIEWPORT,
        "defaultWait": DEFAULT_WAIT,
        "continueOnError": False,
        "steps": steps,
    }
    return task, steps
