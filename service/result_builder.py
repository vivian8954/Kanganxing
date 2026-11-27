# result_builder.py
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from config import PHASES

def load_checkpoint(progress_file: Path) -> Dict[str, Any]:
    if not progress_file.exists():
        return {}
    try:
        return json.loads(progress_file.read_text(encoding="utf-8"))
    except Exception:
        return {}

def build_final_result(
    run_id: str,
    base_url: str,
    user: str,
    headless: bool,
    started: datetime,
    finished: datetime,
    total_elapsed: float,
    phase_result_list: List[Dict],
    all_cli_log: str,
) -> Dict[str, Any]:
    """
    phase_result_list 每个元素：
    {
        "phase_key": "p1",
        "phase_name": "xxx",
        "shot_file": "01_login.png",
        "status": "passed"/"failed"/"skipped",
        "error_msg": "",
        "stdout": "",
        "stderr": "",
        "returncode": int,
        "checkpoint": {},
        "steps": [],
        "screenshot_path": str
    }
    """
    phase_rows = []
    step_rows = []
    prev_t = None
    business = {
        "added_products": [],
        "cart_items": [],
        "order_items": [],
        "subtotal": "",
        "tax": "",
        "total": "",
        "success_header": "",
        "success_text": "",
    }
    passed_count = 0
    failed_count = 0
    skipped_count = 0

    for pr in phase_result_list:
        key = pr["phase_key"]
        label = pr["phase_name"]
        shot_name = pr["shot_file"]
        status = pr["status"]
        cp = pr["checkpoint"]
        if status == "passed":
            passed_count +=1
        elif status == "failed":
            failed_count +=1
        else:
            skipped_count +=1

        cur_t = cp.get(key, {}).get("t") if isinstance(cp.get(key), dict) else None
        duration = (cur_t - prev_t) if (isinstance(cur_t, int) and isinstance(prev_t, int)) else None
        prev_t = cur_t

        detail = ""
        if key == "p1":
            detail = f"{cp.get('title', '')} · {cp.get('url', '')}"
        elif key == "p2":
            detail = f"商品列表 {cp.get('productCount', '?')} 件，账号 {user} 登录成功"
        elif key == "p3":
            products = cp.get("products", [])
            business["added_products"] = products
            detail = "购物车角标 " + str(cp.get("badgeCount", "?")) + " · " + "、".join(
                f"{p.get('name')} {p.get('price')}" for p in products
            )
        elif key == "p4":
            items = cp.get("items", [])
            business["cart_items"] = items
            detail = f"购物车条目 {cp.get('itemCount', '?')} 件：" + "、".join(
                i.get("name", "") for i in items
            )
        elif key == "p5":
            business["order_items"] = cp.get("items", [])
            business["subtotal"] = cp.get("subtotal", "")
            business["tax"] = cp.get("tax", "")
            business["total"] = cp.get("total", "")
            detail = " / ".join(str(cp.get(k, "")) for k in ("subtotal", "tax", "total"))
        elif key == "p6":
            business["success_header"] = cp.get("header", "")
            business["success_text"] = cp.get("text", "")
            detail = cp.get("header", "")
        else:
            detail = pr.get("error_msg", "")

        phase_rows.append({
            "key": key,
            "name": label,
            "status": status,
            "duration_ms": duration,
            "detail": detail,
            "screenshot": pr["screenshot_path"],
            "error_msg": pr.get("error_msg", "")
        })

        # 子步骤加入step列表
        for idx, st in enumerate(pr.get("steps", []), start=1):
            step_status = status
            step_rows.append({
                "index": len(step_rows)+1,
                "phase": label,
                "type": st.get("type"),
                "label": st.get("label", ""),
                "status": step_status,
                "screenshot": st.get("path")
            })

    total_steps = len(step_rows)
    pass_rate = round(passed_count / total_steps *100,1) if total_steps>0 else 0
    all_passed = failed_count ==0

    return {
        "meta": {
            "run_id": run_id,
            "site": base_url,
            "account": user,
            "mode": "headless" if headless else "headed (有头模式)",
            "viewport": "1440x900",
            "engine": "Chromium via Playwright CLI",
            "started_at": started.isoformat(timespec="seconds"),
            "finished_at": finished.isoformat(timespec="seconds"),
            "duration_seconds": round(total_elapsed,2),
            "all_passed": all_passed,
        },
        "summary": {
            "total_steps": total_steps,
            "passed": passed_count,
            "failed": failed_count,
            "skipped": skipped_count,
            "pass_rate": pass_rate,
        },
        "phases": phase_rows,
        "steps": step_rows,
        "business": business,
        "cli_log": all_cli_log[-8000:]
    }
