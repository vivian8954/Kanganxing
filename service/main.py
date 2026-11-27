# main.py
"""
调度入口，核心：阶段隔离，失败不阻断后续
SauceDemo E2E 模块化自动化，单阶段失败不阻断后续
"""
import argparse
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from config import (
    DEFAULT_OUT_DIR, DEFAULT_BROWSER_JS, BASE_URL, DEFAULT_USER, DEFAULT_PASSWORD,
    DEFAULT_FIRST_NAME, DEFAULT_LAST_NAME, DEFAULT_POSTAL_CODE, PHASES
)
from task_builder import build_single_phase_task
from runner import run_browser_task
from result_builder import load_checkpoint, build_final_result
from report_renderer import render_report

def main() -> int:
    parser = argparse.ArgumentParser(description="SauceDemo E2E 模块化自动化，单阶段失败不阻断后续")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="输出根目录")
    parser.add_argument("--browser-js", default=str(DEFAULT_BROWSER_JS), help="browser.js 路径")
    parser.add_argument("--base-url", default=BASE_URL, help="站点地址")
    parser.add_argument("--user", default=DEFAULT_USER, help="登录账号")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help="登录密码")
    parser.add_argument("--first-name", default=DEFAULT_FIRST_NAME)
    parser.add_argument("--last-name", default=DEFAULT_LAST_NAME)
    parser.add_argument("--postal-code", default=DEFAULT_POSTAL_CODE)
    parser.add_argument("--headless", action="store_true", help="无头模式，默认有头")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results").mkdir(exist_ok=True)
    browser_js = Path(args.browser_js)
    if not browser_js.exists():
        print(f"[ERROR] 找不到 browser.js: {browser_js}")
        return 2

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{stamp}_{uuid.uuid4().hex[:6]}"
    shot_dir = out_dir / "screenshots" / stamp
    shot_dir.mkdir(parents=True, exist_ok=True)
    progress_file = out_dir / "results" / f"progress_{stamp}.json"
    task_tmp_file = out_dir / "results" / f"task_{stamp}.json"

    started = datetime.now()
    phase_result_list = []
    all_stdout = ""
    all_stderr = ""
    prev_checkpoint = {}

    print(f"===== 测试开始 run_id={run_id} =====")
    for phase_key, phase_name, shot_filename in PHASES:
        print(f"\n>>> {datetime.now()}正在执行阶段：{phase_name} [{phase_key}]")
        phase_result = {
            "phase_key": phase_key,
            "phase_name": phase_name,
            "shot_file": shot_filename,
            "status": "failed",
            "error_msg": "",
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "checkpoint": {},
            "steps": [],
            "screenshot_path": str(shot_dir / shot_filename)
        }
        try:
            # 构造当前阶段task
            task, steps = build_single_phase_task(
                phase_key=phase_key,
                phase_name=phase_name,
                shot_filename=shot_filename,
                shot_dir=shot_dir,
                progress_path=progress_file,
                user=args.user,
                password=args.password,
                headless=args.headless,
                first_name=args.first_name,
                last_name=args.last_name,
                postal_code=args.postal_code,
                prev_checkpoint=prev_checkpoint
            )
            phase_result["steps"] = steps
            # 写入临时task json
            task_tmp_file.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            # 执行node
            stdout, stderr, retcode = run_browser_task(browser_js, task_tmp_file, timeout=args.timeout)
            phase_result["stdout"] = stdout
            phase_result["stderr"] = stderr
            phase_result["returncode"] = retcode
            all_stdout += f"\n==== {phase_key} stdout ====\n{stdout}"
            all_stderr += f"\n==== {phase_key} stderr ====\n{stderr}"

            if retcode == 0:
                # 读取检查点
                cp = load_checkpoint(progress_file)
                phase_result["checkpoint"] = cp
                phase_result["status"] = "passed"
                prev_checkpoint = cp
                print(f"{datetime.now()}✅ {phase_name} 执行成功")
            else:
                raise Exception(f"node返回码非0: {retcode}, stderr:{stderr[:300]}")
        except Exception as e:
            phase_result["error_msg"] = str(e)
            print(f"❌ {phase_name} 执行失败：{str(e)}")
        phase_result_list.append(phase_result)

    finished = datetime.now()
    total_elapsed = (finished - started).total_seconds()
    print(f"\n===== 全部阶段执行完毕，总耗时：{total_elapsed:.2f}s，开始生成报告 =====")

    # 组装结果
    final_result = build_final_result(
        run_id=run_id,
        base_url=args.base_url,
        user=args.user,
        headless=args.headless,
        started=started,
        finished=finished,
        total_elapsed=total_elapsed,
        phase_result_list=phase_result_list,
        all_cli_log=all_stdout + "\n\n==== STDERR ====\n" + all_stderr
    )
    report_path = out_dir / f"report_{stamp}.html"
    render_report(final_result, report_path, out_dir)
    print(f"🎉 报告生成完成：{report_path}")
    return 0

if __name__ == "__main__":
    exit(main())
