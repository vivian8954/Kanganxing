#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SauceDemo 端到端自动化测试（Playwright CLI 有头模式）+ Gemini 风格可视化报告

使用方式：
    python F:\\Script\\run_saucedemo_test.py
    python F:\\Script\\run_saucedemo_test.py --headless
    python F:\\Script\\run_saucedemo_test.py --user standard_user --password secret_sauce

流程：
    1) 生成带时间戳的任务 JSON，调用 Playwright CLI（browser.js）有头打开站点
    2) 登录 -> 添加两款商品 -> 购物车 -> 收货信息 -> 订单概览 -> 完成结算
    3) 每个阶段做断言并截图，检查点写入 results/progress_<时间戳>.json
    4) 结构化结果写入 results/test_results_<时间戳>.json
    5) 生成单文件可视化报告 report_<时间戳>.html

依赖：
    Node.js + Playwright（技能目录 scripts/node_modules 已包含）
    Python 3.8+（仅标准库）
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

DEFAULT_OUT_DIR = Path(r"F:\Script")
DEFAULT_BROWSER_JS = Path(
    r"C:\Users\yungs\.workbuddy\skills\playwright-browser-automation-engine\scripts\browser.js"
)
BASE_URL = "https://www.saucedemo.com/"
DEFAULT_USER = "standard_user"
DEFAULT_PASSWORD = "secret_sauce"

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


# ---------------------------------------------------------------------------
# 任务构建：给 browser.js 的 task JSON
# ---------------------------------------------------------------------------
def build_task(
    out_dir: Path,
    stamp: str,
    user: str,
    password: str,
    headless: bool,
    first_name: str,
    last_name: str,
    postal_code: str,
) -> tuple[dict, dict]:
    shot_dir = out_dir / "screenshots" / stamp
    progress = out_dir / "results" / f"progress_{stamp}.json"
    ids = json.dumps([p["sku"] for p in PRODUCTS], ensure_ascii=False)
    names = json.dumps([p["name"] for p in PRODUCTS], ensure_ascii=False)
    count = json.dumps(len(PRODUCTS))

    steps: list[dict] = []

    def add(step_type: str, label: str, phase: str = "准备", **kwargs) -> None:
        item = {"type": step_type, "label": label, "phase": phase}
        item.update(kwargs)
        steps.append(item)

    def shot(filename: str) -> str:
        return str(shot_dir / filename).replace("\\", "/")

    def save() -> None:
        add("export", "保存检查点快照", "数据留存", path=str(progress).replace("\\", "/"), format="json")

    # 起始时钟
    add("eval", "记录测试起始时间", js="({t: Date.now()})", var="t0")
    save()

    # 阶段 1：访问首页
    add("goto", "打开 SauceDemo 首页", "访问站点首页", url=BASE_URL, waitUntil="domcontentloaded", timeout=45000)
    add("waitSelector", "等待登录表单渲染", "访问站点首页", selector="#user-name", timeout=30000)
    add("screenshot", "登录页截图", "访问站点首页", path=shot("01_login.png"), full=True)
    add(
        "eval",
        "断言登录页可用",
        "访问站点首页",
        var="p1",
        js="""(() => {
          if (!document.querySelector('#user-name') || !document.querySelector('#login-button')) {
            throw new Error('登录表单元素缺失');
          }
          return {t: Date.now(), url: location.href, title: document.title};
        })()""",
    )
    save()

    # 阶段 2：登录
    add("fill", "填写用户名", "登录 standard_user", selector="#user-name", value=user)
    add("fill", "填写密码", "登录 standard_user", selector="#password", value=password)
    add("click", "点击登录按钮", "登录 standard_user", selector="#login-button")
    add("waitSelector", "等待商品列表出现", "登录 standard_user", selector=".inventory_list", timeout=30000)
    add("screenshot", "商品列表页截图", "登录 standard_user", path=shot("02_inventory.png"), full=True)
    add(
        "eval",
        "断言登录成功与商品数量",
        "登录 standard_user",
        var="p2",
        js="""(() => {
          const url = location.href;
          if (!url.includes('inventory.html')) throw new Error('登录后未进入商品列表: ' + url);
          const n = document.querySelectorAll('.inventory_item').length;
          if (n !== 6) throw new Error('商品数量异常，期望 6，实际 ' + n);
          return {t: Date.now(), url: url, title: document.title, productCount: n};
        })()""",
    )
    save()

    # 阶段 3：加购两款商品
    for product in PRODUCTS:
        add(
            "click",
            f"添加 {product['name']}",
            "添加两款商品",
            selector=f"#add-to-cart-{product['sku']}",
        )
    add("screenshot", "加购后截图", "添加两款商品", path=shot("03_cart_badge.png"), full=True)
    add(
        "eval",
        "断言购物车角标与商品",
        "添加两款商品",
        var="p3",
        js="""(() => {
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
        })()"""
        .replace("__IDS__", ids)
        .replace("__NAMES__", names),
    )
    save()

    # 阶段 4：购物车
    add("click", "进入购物车", "进入购物车核对", selector=".shopping_cart_link")
    add("waitSelector", "等待购物车条目渲染", "进入购物车核对", selector=".cart_item", timeout=30000)
    add("screenshot", "购物车页截图", "进入购物车核对", path=shot("04_cart.png"), full=True)
    add(
        "eval",
        "断言购物车条目",
        "进入购物车核对",
        var="p4",
        js="""(() => {
          if (!location.href.includes('cart.html')) throw new Error('未进入购物车页: ' + location.href);
          const items = Array.from(document.querySelectorAll('.cart_item')).map(function (el) {
            const n = el.querySelector('.inventory_item_name'), p = el.querySelector('.inventory_item_price');
            return {name: n ? n.textContent.trim() : '', price: p ? p.textContent.trim() : ''};
          });
          if (items.length !== __COUNT__)
            throw new Error('购物车商品数量不符，期望 ' + __COUNT__ + '，实际 ' + items.length);
          return {t: Date.now(), url: location.href, itemCount: items.length, items: items};
        })()""".replace("__COUNT__", count),
    )
    save()

    # 阶段 5：收货信息 + 订单概览
    add("click", "进入结算信息页", "填写收货信息 / 订单概览", selector="#checkout")
    add("waitSelector", "等待收货信息表单", "填写收货信息 / 订单概览", selector="#first-name", timeout=30000)
    add("fill", "填写 First Name", "填写收货信息 / 订单概览", selector="#first-name", value=first_name)
    add("fill", "填写 Last Name", "填写收货信息 / 订单概览", selector="#last-name", value=last_name)
    add("fill", "填写 Postal Code", "填写收货信息 / 订单概览", selector="#postal-code", value=postal_code)
    add("click", "提交收货信息", "填写收货信息 / 订单概览", selector="#continue")
    add("waitSelector", "等待订单概览", "填写收货信息 / 订单概览", selector=".summary_info", timeout=30000)
    add("screenshot", "订单概览页截图", "填写收货信息 / 订单概览", path=shot("05_overview.png"), full=True)
    add(
        "eval",
        "断言订单概览与金额",
        "填写收货信息 / 订单概览",
        var="p5",
        js="""(() => {
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
        })()""".replace("__COUNT__", count),
    )
    save()

    # 阶段 6：完成结算
    add("click", "点击 Finish 完成结算", "完成结算", selector="#finish")
    add("waitSelector", "等待结算成功页", "完成结算", selector=".complete-header", timeout=30000)
    add("screenshot", "结算成功页截图", "完成结算", path=shot("06_complete.png"), full=True)
    add(
        "eval",
        "断言结算成功文案",
        "完成结算",
        var="p6",
        js="""(() => {
          if (!location.href.includes('checkout-complete.html'))
            throw new Error('未进入结算完成页: ' + location.href);
          const h = document.querySelector('.complete-header');
          const header = h ? h.textContent.trim() : '';
          if (header !== 'Thank you for your order!') throw new Error('成功文案异常: ' + header);
          const d = document.querySelector('.complete-text');
          return {t: Date.now(), url: location.href, header: header,
                  text: d ? d.textContent.trim() : ''};
        })()""",
    )
    save()

    task = {
        "url": BASE_URL,
        "headless": headless,
        "engine": "chromium",
        "viewport": {"width": 1440, "height": 900},
        "defaultWait": 350,
        "continueOnError": False,
        "steps": steps,
        "outputVars": str(out_dir / "results" / f"vars_{stamp}.json").replace("\\", "/"),
    }
    meta = {
        "progress": str(progress),
        "shot_dir": str(shot_dir),
        "shot_files": {key: filename for key, _label, filename in PHASES},
    }
    return task, meta


# ---------------------------------------------------------------------------
# 执行与结果整理
# ---------------------------------------------------------------------------
def run_cli(browser_js: Path, task_file: Path, timeout: int = 600) -> tuple[str, str, int]:
    cmd = ["node", str(browser_js), "--task-file", str(task_file)]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return proc.stdout or "", proc.stderr or "", proc.returncode


def build_result(
    task: dict,
    out_dir: Path,
    stamp: str,
    started: datetime,
    finished: datetime,
    started_ts: float,
    stdout: str,
    stderr: str,
    returncode: int,
    headless: bool,
    progress_file: Path,
    user: str,
) -> dict:
    steps = task["steps"]
    failure = re.search(r"\[step (\d+) 失败\]\s*(.+)", stdout)
    failed_index = int(failure.group(1)) if failure else None
    failure_message = failure.group(2).strip() if failure else ""

    step_rows = []
    for i, step in enumerate(steps, start=1):
        if failed_index is None:
            status = "passed"
        elif i < failed_index:
            status = "passed"
        elif i == failed_index:
            status = "failed"
        else:
            status = "skipped"
        screenshot = step.get("path") if step.get("type") == "screenshot" else None
        step_rows.append(
            {
                "index": i,
                "phase": step.get("phase", "准备"),
                "type": step.get("type"),
                "label": step.get("label", ""),
                "status": status,
                "screenshot": screenshot,
            }
        )

    checkpoints: dict = {}
    if progress_file.exists():
        try:
            checkpoints = json.loads(progress_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            checkpoints = {}

    phase_rows = []
    prev_t = checkpoints.get("t0", {}).get("t") if isinstance(checkpoints.get("t0"), dict) else None
    for key, label, filename in PHASES:
        cp = checkpoints.get(key)
        if not isinstance(cp, dict):
            phase_rows.append(
                {"key": key, "name": label, "status": "failed" if failed_index else "pending",
                 "duration_ms": None, "detail": "未到达该阶段", "screenshot": None}
            )
            continue
        cur_t = cp.get("t")
        duration = (cur_t - prev_t) if (isinstance(cur_t, int) and isinstance(prev_t, int)) else None
        prev_t = cur_t
        if key == "p1":
            detail = f"{cp.get('title', '')} · {cp.get('url', '')}"
        elif key == "p2":
            detail = f"商品列表 {cp.get('productCount', '?')} 件，账号 {user} 登录成功"
        elif key == "p3":
            products = cp.get("products", [])
            detail = "购物车角标 " + str(cp.get("badgeCount", "?")) + " · " + "、".join(
                f"{p.get('name')} {p.get('price')}" for p in products
            )
        elif key == "p4":
            detail = f"购物车条目 {cp.get('itemCount', '?')} 件：" + "、".join(
                i.get("name", "") for i in cp.get("items", [])
            )
        elif key == "p5":
            detail = " / ".join(
                str(cp.get(k, "")) for k in ("subtotal", "tax", "total")
            )
        else:
            detail = cp.get("header", "")
        phase_rows.append(
            {
                "key": key,
                "name": label,
                "status": "passed",
                "duration_ms": duration,
                "detail": detail,
                "screenshot": str(out_dir / "screenshots" / stamp / filename),
            }
        )

    passed = sum(1 for s in step_rows if s["status"] == "passed")
    failed = sum(1 for s in step_rows if s["status"] == "failed")
    skipped = sum(1 for s in step_rows if s["status"] == "skipped")
    success = returncode == 0 and failed == 0 and all(p["status"] == "passed" for p in phase_rows)

    p3 = checkpoints.get("p3") if isinstance(checkpoints.get("p3"), dict) else {}
    p4 = checkpoints.get("p4") if isinstance(checkpoints.get("p4"), dict) else {}
    p5 = checkpoints.get("p5") if isinstance(checkpoints.get("p5"), dict) else {}
    p6 = checkpoints.get("p6") if isinstance(checkpoints.get("p6"), dict) else {}

    return {
        "meta": {
            "run_id": stamp,
            "site": BASE_URL,
            "account": user,
            "mode": "headless" if headless else "headed (有头模式)",
            "viewport": "1440x900",
            "engine": "Chromium via Playwright CLI",
            "started_at": started.isoformat(timespec="seconds"),
            "finished_at": finished.isoformat(timespec="seconds"),
            "duration_seconds": round(time.monotonic() - started_ts, 2),
            "browser_js": str(DEFAULT_BROWSER_JS),
            "cli_exit_code": returncode,
            "all_passed": success,
        },
        "summary": {
            "total_steps": len(step_rows),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_rate": round(passed / len(step_rows) * 100, 1) if step_rows else 0,
            "failure_message": failure_message,
        },
        "phases": phase_rows,
        "steps": step_rows,
        "business": {
            "added_products": p3.get("products", []),
            "cart_items": p4.get("items", []),
            "order_items": p5.get("items", []),
            "subtotal": p5.get("subtotal", ""),
            "tax": p5.get("tax", ""),
            "total": p5.get("total", ""),
            "success_header": p6.get("header", ""),
            "success_text": p6.get("text", ""),
        },
        "checkpoints": checkpoints,
        "cli_log": (stdout + ("\n" + stderr if stderr else ""))[-8000:],
    }


# ---------------------------------------------------------------------------
# Gemini 风格可视化报告
# ---------------------------------------------------------------------------
CSS = r"""
:root{
  --blue:#4285f4;--purple:#9b72cb;--pink:#d96570;--green:#34a853;--red:#ea4335;--yellow:#fbbc05;
  --ink:#202124;--ink2:#5f6368;--ink3:#80868b;--line:#e8eaed;--bg:#f6f8fc;--card:#fff;
  --grad:linear-gradient(120deg,#4285f4 0%,#9b72cb 55%,#d96570 100%);
  --shadow:0 8px 30px rgba(60,64,67,.08);--shadow-hi:0 18px 48px rgba(60,64,67,.14);
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Google Sans','Product Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Microsoft YaHei',sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1180px;margin:0 auto;padding:0 26px 72px}
.hero{position:relative;overflow:hidden;padding:58px 0 48px;border-radius:0 0 40px 40px;
  background:linear-gradient(135deg,#fff 0%,#f2f5ff 52%,#fdf2f6 100%);box-shadow:0 10px 40px rgba(60,64,67,.05);margin-bottom:40px}
.orb{position:absolute;border-radius:50%;filter:blur(72px);opacity:.42;animation:float 16s ease-in-out infinite}
.orb.a{width:390px;height:390px;background:#bfd4ff;top:-160px;left:-100px}
.orb.b{width:330px;height:330px;background:#e2ccff;top:-50px;right:-80px;animation-delay:-5s}
.orb.c{width:290px;height:290px;background:#ffd2df;bottom:-170px;left:42%;animation-delay:-10s}
@keyframes float{0%,100%{transform:translate(0,0)}50%{transform:translate(26px,-24px)}}
.hero-in{position:relative;z-index:2;max-width:1180px;margin:0 auto;padding:0 26px}
.brand{display:flex;align-items:center;gap:12px;margin-bottom:22px}
.brand svg{width:38px;height:38px;filter:drop-shadow(0 5px 12px rgba(155,114,203,.35))}
.brand span{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink2);font-weight:700}
.hero h1{font-size:clamp(30px,5vw,50px);line-height:1.16;letter-spacing:-.025em;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{margin-top:12px;color:var(--ink2);font-size:16px;max-width:720px}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.chip{display:inline-flex;align-items:center;gap:8px;padding:8px 15px;border-radius:999px;background:rgba(255,255,255,.88);
  border:1px solid var(--line);font-size:13px;color:var(--ink2);box-shadow:0 2px 10px rgba(60,64,67,.05);backdrop-filter:blur(6px)}
.chip b{color:var(--ink);font-weight:650}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.dot.g{background:var(--green);box-shadow:0 0 0 4px rgba(52,168,83,.14)}
.dot.r{background:var(--red);box-shadow:0 0 0 4px rgba(234,67,53,.14)}
.sec{margin-top:46px}
.sec-h{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.sec-h .bar{width:4px;height:24px;border-radius:4px;background:var(--grad)}
.sec-h h2{font-size:21px;font-weight:680;letter-spacing:-.01em}
.sec-h .hint{margin-left:auto;font-size:12px;color:var(--ink3)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}
.stat{position:relative;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:20px 20px 18px;
  box-shadow:var(--shadow);overflow:hidden;opacity:0;animation:rise .55s ease forwards;transition:transform .25s,box-shadow .25s}
.stat:hover{transform:translateY(-5px);box-shadow:var(--shadow-hi)}
.stat:nth-child(1){animation-delay:.04s}.stat:nth-child(2){animation-delay:.11s}.stat:nth-child(3){animation-delay:.18s}
.stat:nth-child(4){animation-delay:.25s}.stat:nth-child(5){animation-delay:.32s}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
.stat::after{content:"";position:absolute;inset:0 0 auto 0;height:3px;background:var(--grad)}
.stat .k{font-size:12px;color:var(--ink3);font-weight:600;letter-spacing:.04em}
.stat .v{font-size:29px;font-weight:720;letter-spacing:-.02em;margin-top:8px;line-height:1.2}
.stat .s{font-size:12px;color:var(--ink3);margin-top:5px}
.v.good{color:var(--green)}.v.bad{color:var(--red)}
.grid2{display:grid;grid-template-columns:minmax(280px,.85fr) minmax(320px,1.15fr);gap:18px}
@media(max-width:860px){.grid2{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px;box-shadow:var(--shadow)}
.card h3{font-size:15px;font-weight:680;margin-bottom:18px}
.donut-wrap{display:flex;align-items:center;gap:24px;flex-wrap:wrap}
.donut{width:132px;height:132px;border-radius:50%;display:grid;place-items:center;position:relative;flex:none}
.donut::after{content:"";position:absolute;inset:16px;border-radius:50%;background:#fff;box-shadow:inset 0 2px 10px rgba(60,64,67,.08)}
.donut .inner{position:relative;z-index:2;text-align:center}
.donut .inner b{font-size:25px;letter-spacing:-.02em}.donut .inner small{display:block;color:var(--ink3);font-size:11px}
.legend{font-size:13px;color:var(--ink2);display:grid;gap:9px}
.legend div{display:flex;align-items:center;gap:9px}
.bars{display:grid;gap:15px}
.bar-row{display:grid;grid-template-columns:120px 1fr 58px;align-items:center;gap:12px;font-size:12px;color:var(--ink2)}
.track{height:9px;border-radius:99px;background:#eef0f4;overflow:hidden}
.fill{height:100%;border-radius:99px;background:var(--grad);width:0;transition:width 1s cubic-bezier(.2,.8,.2,1)}
.bar-row .val{text-align:right;color:var(--ink);font-weight:650;font-variant-numeric:tabular-nums}
.timeline{position:relative;padding-left:8px}
.timeline::before{content:"";position:absolute;left:19px;top:14px;bottom:14px;width:2px;background:linear-gradient(#4285f4,#9b72cb,#e8eaed)}
.tl-item{position:relative;display:flex;gap:18px;padding:0 0 22px 0}
.tl-item:last-child{padding-bottom:0}
.tl-dot{width:24px;height:24px;border-radius:50%;background:var(--green);border:4px solid #e8f5e9;flex:none;z-index:2;margin-top:16px}
.tl-dot.fail{background:var(--red);border-color:#fdecea}
.tl-dot.pending{background:#bdc1c6;border-color:#f1f3f4}
.tl-body{flex:1;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 20px;box-shadow:var(--shadow)}
.tl-toggle{display:flex;align-items:center;gap:12px;width:100%;background:none;border:none;padding:0;
  font:inherit;color:inherit;cursor:pointer;text-align:left}
.tl-toggle b{font-size:15px}
.tl-toggle .t{font-size:12px;color:var(--ink3);margin-left:auto;font-variant-numeric:tabular-nums}
.tl-toggle .arrow{font-size:13px;color:var(--ink3);transition:transform .25s ease;margin-left:10px}
.tl-item.open .tl-toggle .arrow{transform:rotate(180deg)}
.tl-detail{font-size:13px;color:var(--ink2);margin-top:6px;word-break:break-all}
.tl-collapse{display:none;margin-top:12px}
.tl-item.open .tl-collapse{display:block}
.tl-thumb{max-width:100%;border-radius:12px;border:1px solid var(--line);cursor:zoom-in;transition:transform .2s ease}
.tl-thumb:hover{transform:scale(1.02)}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;font-weight:700;letter-spacing:.03em}
.badge.ok{background:#e6f4ea;color:#137333}.badge.no{background:#fce8e6;color:#c5221f}.badge.wait{background:#f1f3f4;color:#5f6368}
.step-scroll{max-height:430px;overflow:auto;border-radius:14px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:12px 14px;color:var(--ink3);font-weight:650;font-size:11px;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid var(--line)}
td{padding:11px 14px;border-bottom:1px solid #f1f3f4;color:var(--ink2)}
tr:last-child td{border-bottom:0}
tbody tr:hover{background:#fafbff}
td.idx{color:var(--ink3);font-variant-numeric:tabular-nums;width:42px}
.products{display:grid;gap:10px}
.product{display:flex;align-items:center;gap:12px;padding:11px 14px;border:1px solid var(--line);border-radius:14px;background:#fafbff}
.product .ic{width:34px;height:34px;border-radius:10px;background:var(--grad);display:grid;place-items:center;color:#fff;flex:none}
.product .nm{font-size:13px;font-weight:600;color:var(--ink)}
.product .pr{margin-left:auto;font-size:13px;font-weight:680;color:var(--ink)}
.totals{display:grid;gap:8px;margin-top:16px;font-size:13px}
.totals div{display:flex;justify-content:space-between;color:var(--ink2)}
.totals div.last{padding-top:10px;border-top:1px dashed var(--line);font-size:15px;font-weight:700;color:var(--ink)}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.shot{background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;box-shadow:var(--shadow)}
.shot{background:#fafbff}
.shot img{width:100%;height:150px;object-fit:cover;object-position:top;display:block;cursor:zoom-in;transition:transform .4s}
.shot:hover img{transform:scale(1.03)}
.shot figcaption{padding:10px 14px;font-size:12px;color:var(--ink2);border-top:1px solid var(--line)}
.lightbox{position:fixed;inset:0;z-index:100;display:grid;place-items:center;background:rgba(32,33,36,.82);padding:32px;cursor:zoom-out}
.lightbox[hidden]{display:none}
.lightbox-img{max-width:100%;max-height:100%;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,.45);user-select:none}
details{margin-top:16px;font-size:12px;color:var(--ink2)}
summary{cursor:pointer;font-weight:600;color:var(--ink)}
pre{margin-top:10px;background:#202124;color:#e8eaed;padding:16px;border-radius:14px;max-height:280px;overflow:auto;font-size:11px;line-height:1.55;white-space:pre-wrap;word-break:break-all}
footer{margin-top:52px;text-align:center;font-size:12px;color:var(--ink3)}
@media print{.orb{display:none}.hero{border-radius:0}.stat,.tl-body,.card{box-shadow:none;opacity:1}.step-scroll{max-height:none;overflow:visible}body{background:#fff}.lightbox{display:none!important}}
"""

SVG_BRAND = """<svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="g" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#4285f4"/><stop offset=".55" stop-color="#9b72cb"/><stop offset="1" stop-color="#d96570"/></linearGradient></defs>
<path d="M20 2l3.6 10.4L34 16l-10.4 3.6L20 30l-3.6-10.4L6 16l10.4-3.6L20 2z" fill="url(#g)"/>
<circle cx="31" cy="30" r="4" fill="#fbbc05"/><circle cx="8" cy="31" r="2.6" fill="#34a853"/></svg>"""


def render_report(result: dict, report_path: Path, out_dir: Path) -> None:
    esc = lambda v: html.escape(str(v) if v is not None else "", quote=True)
    meta, summary = result["meta"], result["summary"]
    business = result["business"]
    ok = bool(meta["all_passed"])

    def rel(path: str | None) -> str:
        if not path:
            return ""
        try:
            return Path(path).relative_to(out_dir).as_posix()
        except ValueError:
            return Path(path).as_posix()

    pass_rate = summary["pass_rate"]
    fail_rate = round(summary["failed"] / summary["total_steps"] * 100, 1) if summary["total_steps"] else 0.0
    donut = (
        f"conic-gradient(#34a853 0 {pass_rate}%, #ea4335 {pass_rate}% {pass_rate + fail_rate}%, "
        f"#e8eaed {pass_rate + fail_rate}% 100%)"
    )

    durations = [p.get("duration_ms") or 0 for p in result["phases"]]
    max_dur = max(durations) if durations else 1

    parts: list[str] = []
    parts.append("<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'>")
    parts.append("<meta name='viewport' content='width=device-width,initial-scale=1.0'>")
    parts.append("<title>SauceDemo 自动化测试报告 · " + esc(meta["run_id"]) + "</title>")
    parts.append("<style>" + CSS + "</style></head><body>")
    parts.append("<header class='hero'><div class='orb a'></div><div class='orb b'></div><div class='orb c'></div><div class='hero-in'>")
    parts.append("<div class='brand'>" + SVG_BRAND + "<span>Test Intelligence · SauceDemo E2E</span></div>")
    parts.append("<h1>端到端自动化测试报告</h1>")
    parts.append("<p>Playwright CLI 有头模式驱动真实浏览器，完整走通登录、加购、购物车、收货信息与结算流程。</p>")
    parts.append("<div class='chips'>")
    dot_cls = "g" if ok else "r"
    verdict = "通过" if ok else "失败"
    parts.append(f"<span class='chip'><span class='dot {dot_cls}'></span>结果 <b>{verdict}</b></span>")
    parts.append(f"<span class='chip'>测试轮次 <b>{esc(meta['run_id'])}</b></span>")
    parts.append(f"<span class='chip'>站点 <b>{esc(meta['site'])}</b></span>")
    parts.append(f"<span class='chip'>账号 <b>{esc(meta['account'])}</b></span>")
    parts.append(f"<span class='chip'>模式 <b>{esc(meta['mode'])}</b></span>")
    parts.append("</div></div></header><main class='wrap'>")

    # 指标卡
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>核心指标</h2><span class='hint'>本轮数据概览</span></div><div class='stats'>")
    stat_data = [
        ("总体结果", "PASS" if ok else "FAIL", "good" if ok else "bad", f"CLI 退出码 {meta['cli_exit_code']}"),
        ("步骤通过率", f"{pass_rate}%", "", f"{summary['passed']} / {summary['total_steps']} 步通过"),
        ("执行步骤", str(summary["total_steps"]), "", f"失败 {summary['failed']} · 跳过 {summary['skipped']}"),
        ("总耗时", f"{meta['duration_seconds']}s", "", "含浏览器启动与截图"),
        ("订单总额", esc(business.get("total") or "—"), "", "结算页金额"),
    ]
    for k, v, cls, s in stat_data:
        parts.append(f"<div class='stat'><div class='k'>{esc(k)}</div><div class='v {cls}'>{v}</div><div class='s'>{esc(s)}</div></div>")
    parts.append("</div></section>")

    # 通过率 + 阶段耗时
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>执行质量与耗时</h2><span class='hint'>按阶段统计</span></div><div class='grid2'>")
    parts.append("<div class='card'><h3>步骤通过率</h3><div class='donut-wrap'>")
    parts.append(f"<div class='donut' style='background:{donut}'><div class='inner'><b>{pass_rate}%</b><small>通过率</small></div></div>")
    parts.append("<div class='legend'>")
    parts.append(f"<div><span class='dot g'></span>通过 {summary['passed']} 步</div>")
    parts.append(f"<div><span class='dot r'></span>失败 {summary['failed']} 步</div>")
    parts.append(f"<div><span style='width:8px;height:8px;border-radius:50%;display:inline-block;background:#bdc1c6'></span>未执行 {summary['skipped']} 步</div>")
    parts.append("</div></div></div>")
    parts.append("<div class='card'><h3>各阶段耗时（毫秒）</h3><div class='bars'>")
    for p in result["phases"]:
        dur = p.get("duration_ms") or 0
        width = min(100, round(dur / max_dur * 100)) if max_dur else 0
        parts.append(
            f"<div class='bar-row'><span>{esc(p['name'])}</span><div class='track'>"
            f"<div class='fill' data-w='{width}'></div></div><span class='val'>{dur}</span></div>"
        )
    parts.append("</div></div></div></section>")

    # 阶段时间线（默认折叠，展开显示缩略图，点击缩略图当前页放大）
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>流程时间线</h2><span class='hint'>点击箭头展开缩略图，点击图片当前页放大</span></div><div class='timeline'>")
    for p in result["phases"]:
        state = p["status"]
        cls = "fail" if state == "failed" else ("pending" if state != "passed" else "")
        badge = {"passed": ("ok", "通过"), "failed": ("no", "失败")}.get(state, ("wait", "未执行"))
        screenshot = rel(p.get("screenshot"))
        thumb_html = ""
        if screenshot:
            thumb_html = (
                "<div class='tl-collapse'>"
                f"<img class='tl-thumb' src='{esc(screenshot)}' alt='{esc(p['name'])}' data-lightbox='{esc(screenshot)}'>"
                "</div>"
            )
        parts.append(
            f"<div class='tl-item'><div class='tl-dot {cls}'></div><div class='tl-body'>"
            f"<button class='tl-toggle' type='button'>"
            f"<span class='badge {badge[0]}'>{badge[1]}</span><b>{esc(p['name'])}</b>"
            f"<span class='t'>{p.get('duration_ms') or '—'} ms</span><span class='arrow'>▾</span>"
            f"</button>"
            f"<div class='tl-detail'>{esc(p.get('detail'))}</div>"
            f"{thumb_html}</div></div>"
        )
    parts.append("</div></section>")

    # 步骤明细 + 订单信息
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>步骤明细</h2><span class='hint'>共 " + str(summary["total_steps"]) + " 步 · 可滚动</span></div><div class='card'><div class='step-scroll'><table>")
    parts.append("<thead><tr><th>#</th><th>阶段</th><th>操作</th><th>类型</th><th>状态</th></tr></thead><tbody>")
    for s in result["steps"]:
        badge = {"passed": ("ok", "通过"), "failed": ("no", "失败"), "skipped": ("wait", "跳过")}[s["status"]]
        parts.append(
            f"<tr><td class='idx'>{s['index']}</td><td>{esc(s['phase'])}</td><td>{esc(s['label'])}</td>"
            f"<td>{esc(s['type'])}</td><td><span class='badge {badge[0]}'>{badge[1]}</span></td></tr>"
        )
    parts.append("</tbody></table></div>")
    if summary.get("failure_message"):
        parts.append("<details open><summary>失败原因</summary><pre>" + esc(summary["failure_message"]) + "</pre></details>")
    parts.append("</div></section>")

    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>业务数据核对</h2><span class='hint'>商品与金额</span></div><div class='grid2'>")
    parts.append("<div class='card'><h3>已加入购物车的商品</h3><div class='products'>")
    products = business.get("added_products") or []
    if not products:
        parts.append("<div style='font-size:13px;color:var(--ink3)'>未采集到商品数据</div>")
    for p in products:
        parts.append(
            "<div class='product'><div class='ic'>✦</div><div class='nm'>" + esc(p.get("name"))
            + "</div><div class='pr'>" + esc(p.get("price")) + "</div></div>"
        )
    parts.append("</div></div>")
    parts.append("<div class='card'><h3>订单金额</h3><div class='totals'>")
    for label, key in (("商品小计", "subtotal"), ("税费", "tax")):
        parts.append(f"<div><span>{label}</span><b>{esc(business.get(key) or '—')}</b></div>")
    parts.append(f"<div class='last'><span>合计</span><b>{esc(business.get('total') or '—')}</b></div>")
    parts.append("</div><div style='margin-top:18px;font-size:13px;color:var(--ink2)'>")
    parts.append("结算结果：<b style='color:" + ("var(--green)" if ok else "var(--red)") + "'>"
                 + esc(business.get("success_header") or "未完成") + "</b></div></div></section>")

    # 截图证据（点击在当前页放大，不再新开标签页）
    parts.append("<section class='sec'><div class='sec-h'><i class='bar'></i><h2>过程证据</h2><span class='hint'>点击图片当前页放大，再次点击关闭</span></div><div class='gallery'>")
    for p in result["phases"]:
        src = rel(p.get("screenshot"))
        if not src:
            continue
        parts.append(f"<figure class='shot'>"
                     f"<img src='{esc(src)}' alt='{esc(p['name'])}' data-lightbox='{esc(src)}'>")
        parts.append(f"<figcaption>{esc(p['name'])}</figcaption></figure>")
    parts.append("</div>")
    parts.append("<details><summary>查看 CLI 原始日志</summary><pre>" + esc(result.get("cli_log", "")) + "</pre></details>")
    parts.append("</section>")

    # 图片放大预览层（当前页内 Lightbox，不跳转新页面）
    parts.append("<div class='lightbox' id='lightbox' hidden>"
                 "<img class='lightbox-img' id='lightbox-img' alt='放大预览'></div>")

    parts.append("<footer>Generated by run_saucedemo_test.py · " + esc(meta["finished_at"])
                 + " · Run ID " + esc(meta["run_id"]) + "</footer>")
    parts.append("</main>")
    parts.append("""<script>
(function () {
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lightbox-img');

  function openLightbox(src, alt) {
    lbImg.src = src;
    lbImg.alt = alt || '放大预览';
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    lb.hidden = true;
    lbImg.src = '';
    document.body.style.overflow = '';
  }

  // 点击带 data-lightbox 的图片：当前页放大
  document.addEventListener('click', function (e) {
    var img = e.target.closest('[data-lightbox]');
    if (img) {
      openLightbox(img.getAttribute('data-lightbox'), img.alt);
      return;
    }
    // 点击遮罩或放大图本身：关闭，回到页面
    if (e.target.closest('.lightbox')) {
      closeLightbox();
    }
  });

  // Esc 关闭预览
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeLightbox(); }
  });

  // 时间线折叠 / 展开
  document.querySelectorAll('.tl-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.tl-item');
      if (item) { item.classList.toggle('open'); }
    });
  });

  // 耗时条形图动画
  setTimeout(function () {
    document.querySelectorAll('.fill').forEach(function (el) {
      el.style.width = el.dataset.w + '%';
    });
  }, 120);
})();
</script>""")
    parts.append("</body></html>")

    report_path.write_text("\n".join(parts), encoding="utf-8")


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main() -> int:
    global BASE_URL
    parser = argparse.ArgumentParser(description="SauceDemo CLI 自动化测试 + 可视化报告")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="输出根目录")
    parser.add_argument("--browser-js", default=str(DEFAULT_BROWSER_JS), help="browser.js 路径")
    parser.add_argument("--base-url", default=BASE_URL, help="站点地址")
    parser.add_argument("--user", default=DEFAULT_USER, help="登录账号")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="登录密码")
    parser.add_argument("--first-name", default="Test", help="收货 First Name")
    parser.add_argument("--last-name", default="User", help="收货 Last Name")
    parser.add_argument("--postal-code", default="100001", help="邮编")
    parser.add_argument("--headless", action="store_true", help="使用无头模式（默认有头）")
    parser.add_argument("--timeout", type=int, default=600, help="CLI 超时秒数")
    args = parser.parse_args()

    BASE_URL = args.base_url
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results").mkdir(exist_ok=True)
    browser_js = Path(args.browser_js)
    if not browser_js.exists():
        print(f"[ERROR] 找不到 Playwright CLI: {browser_js}", file=sys.stderr)
        return 2

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    started = datetime.now()
    started_ts = time.monotonic()

    task, aux = build_task(
        out_dir, stamp, args.user, args.password, args.headless,
        args.first_name, args.last_name, args.postal_code,
    )
    task_file = out_dir / f"task_{stamp}.json"
    task_file.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] 运行编号: {stamp}")
    print(f"[INFO] 模式: {'headless' if args.headless else '有头模式'}")
    print("[INFO] 正在调用 Playwright CLI ...")
    stdout, stderr, code = run_cli(browser_js, task_file, args.timeout)
    log_file = out_dir / f"cli_log_{stamp}.log"
    log_file.write_text(stdout + ("\n" + stderr if stderr else ""), encoding="utf-8")
    print(stdout.strip())
    if stderr.strip():
        print(stderr.strip(), file=sys.stderr)

    finished = datetime.now()
    result = build_result(
        task, out_dir, stamp, started, finished, started_ts,
        stdout, stderr, code, args.headless,
        Path(aux["progress"]), args.user,
    )
    result_path = out_dir / "results" / f"test_results_{stamp}.json"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = out_dir / f"test_report_{stamp}.html"
    render_report(result, report_path, out_dir)

    s = result["summary"]
    print(f"[RESULT] 总体: {'PASS' if result['meta']['all_passed'] else 'FAIL'}")
    print(f"[RESULT] 步骤: {s['passed']}/{s['total_steps']} 通过，失败 {s['failed']}，跳过 {s['skipped']}")
    if s.get("failure_message"):
        print("[RESULT] 失败原因: " + s["failure_message"])
    print(f"[FILE] 结果数据: {result_path}")
    print(f"[FILE] 可视化报告: {report_path}")
    print(f"[FILE] CLI 日志: {log_file}")
    return 0 if result["meta"]["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
