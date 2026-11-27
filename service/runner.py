# runner.py
import subprocess
from pathlib import Path
from typing import Tuple

def run_browser_task(
    browser_js: Path,
    task_file: Path,
    timeout: int = 600
) -> Tuple[str, str, int]:
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
